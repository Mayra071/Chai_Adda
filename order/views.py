from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from .models import Order
from chai.models import ChaiVariety
from payment.models import Payment

@login_required
def create_order(request, chai_id):
    chai = get_object_or_404(ChaiVariety, id=chai_id)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            sugar_level = request.POST.get('sugar_level', 'normal')
            total_price = chai.price * quantity

            order = Order.objects.create(
                chai=chai,
                customer_name=request.user.get_full_name() if request.user.is_authenticated else 'Guest',
                quantity=quantity,
                sugar_level=sugar_level,
                total_price=total_price
            )
            
            # Create payment for the order
            payment = Payment.objects.create(
                user=request.user,
                chai=chai,
                amount=total_price,
                payment_status='PENDING'
            )
            order.payment = payment
            order.save()
            
            messages.success(request, 'Order created successfully!')
            return redirect('payment:payment_process', payment_id=payment.id)
            
        except Exception as e:
            messages.error(request, f'Error creating order: {str(e)}')
            return redirect('chai:chai_detail', chai_id=chai_id)
    
    return render(request, 'order/create_order.html', {'chai': chai})

@login_required
def submit_order(request):
    if request.method == 'POST':
        try:
            chai_id = request.POST.get('chai_id')
            quantity = int(request.POST.get('quantity', 1))
            sugar_level = request.POST.get('sugar_level', 'normal')
            
            chai = get_object_or_404(ChaiVariety, id=chai_id)
            total_price = chai.price * quantity

            order = Order.objects.create(
                user=request.user,
                chai=chai,
                customer_name=request.user.get_full_name(),
                quantity=quantity,
                sugar_level=sugar_level,
                total_price=total_price
            )
            
            messages.success(request, 'Order created successfully! Please proceed with payment.')
            return redirect('payment:payment_options', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f'Error submitting order: {str(e)}')
            return redirect('chai:all_chai')
    
    return redirect('chai:all_chai')

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/confirmation.html', {'order': order})

@login_required
def order_history(request):
    search_query = request.GET.get('search', '')
    orders = Order.objects.filter(
        customer_name=request.user.get_full_name()
    ).select_related('chai', 'payment').order_by('-ordered_at')
    
    if search_query:
        orders = orders.filter(
            Q(chai__name__icontains=search_query) |
            Q(payment_status__icontains=search_query)
        )
    
    return render(request, 'order/history.html', {
        'orders': orders,
        'search_query': search_query
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/order_detail.html', {
        'order': order,
        'payment': order.payment
    })
