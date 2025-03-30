from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import ChaiVariety, Store, ChaiReview
from .forms import StoreSearchForm, ChaiReviewForm
from payment.models import Payment
from order.models import Order
from django.urls import reverse
import uuid
from django.db import transaction

def order_chai(request, chai_id):
    chai = get_object_or_404(ChaiVariety, pk=chai_id)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            sugar_level = request.POST.get('sugar_level', 'normal')
            customer_name = request.POST.get('name', 'Guest')
            
            if quantity < 1:
                messages.error(request, 'Quantity must be at least 1')
                return redirect('chai:chai_detail', chai_id=chai_id)
            
            # Calculate total price
            total_price = chai.price * quantity
            
            # Create the order and payment in one transaction
            with transaction.atomic():
                # Create payment first with UPI as default payment mode
                payment = Payment.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    amount=total_price,
                    payment_status='PENDING',
                    payment_mode='UPI',  # Set UPI as default payment mode
                    transaction_id=f"CHAI-{uuid.uuid4().hex[:8].upper()}"
                )
                
                # Create and link order
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    chai=chai,
                    customer_name=customer_name,
                    quantity=quantity,
                    sugar_level=sugar_level,
                    total_price=total_price,
                    payment_status='unpaid',
                    payment=payment
                )
            
            # Redirect directly to payment gateway instead of payment options
            return redirect('payment:payment_gateway', payment_id=payment.id)
            
        except Exception as e:
            messages.error(request, f'Error processing order: {str(e)}')
            return redirect('chai:chai_detail', chai_id=chai_id)
    
    return render(request, 'chai/order.html', {'chai': chai})

def all_chai(request):
    search_query = request.GET.get('search', '')
    chais = ChaiVariety.objects.all()
    
    if search_query:
        chais = chais.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(chai_type__icontains=search_query)
        )
    
    return render(request, 'chai/all_chai.html', {
        'chais': chais,
        'search_query': search_query
    })

def chai_detail(request, chai_id):
    chai = get_object_or_404(ChaiVariety, pk=chai_id)
    reviews = chai.reviews.all().select_related('user').order_by('-date_added')
    
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating:
            ChaiReview.objects.create(
                chai=chai,
                user=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Thank you for your review!')
            return redirect('chai:chai_detail', chai_id=chai_id)
    
    return render(request, 'chai/chai_detail.html', {
        'chai': chai,
        'reviews': reviews,
        'average_rating': chai.reviews.aggregate(Avg('rating'))['rating__avg']
    })

def store_view(request):
    form = StoreSearchForm(request.GET)
    stores = Store.objects.filter(is_active=True).prefetch_related('chai_varieties')
    
    if form.is_valid():
        location = form.cleaned_data.get('location')
        chai_type = form.cleaned_data.get('chai_type')
        
        if location:
            stores = stores.filter(location__icontains=location)
        if chai_type:
            stores = stores.filter(chai_varieties__chai_type=chai_type).distinct()
    
    # Group stores by location
    locations = {}
    for store in stores:
        if store.location not in locations:
            locations[store.location] = []
        locations[store.location].append({
            'name': store.name,
            'address': store.address,
            'phone': store.phone,
            'email': store.email,
            'is_open': store.is_open(),
            'chai_varieties': [
                {'name': cv.name, 'type': cv.get_chai_type_display(), 'price': cv.price}
                for cv in store.chai_varieties.all()
            ]
        })
    
    context = {
        'form': form,
        'locations': locations,
        'total_stores': stores.count()
    }
    return render(request, 'chai/store_view.html', context)