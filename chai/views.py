from django.shortcuts import render, get_object_or_404, redirect

from .models import Chai_varity, Store
from .forms import Chai_varity_Form  # Ensure the correct form name is used

# def order_chai(request, chai_id):
#     if request.method == "POST":
#         quantity = request.POST.get('quantity')
#         preferences = request.POST.get('preferences')
#         # Here you would typically handle the order logic, e.g., saving to the database
#         # For now, we will just redirect to the all_chai view after submission
#         return redirect('chai:all_chai')


def all_chai(request):

    chais = Chai_varity.objects.all()
    return render(request, 'chai/all_chai.html', {'chais': chais})

def chai_detail(request, chai_id):
    chai = get_object_or_404(Chai_varity, pk=chai_id)
    return render(request, 'chai/chai_detail.html', {'chai': chai})

def chai_store_view(request):
    stores = None
    form = Chai_varity_Form()  # Initialize the form variable
    if request.method == 'POST':
        form = Chai_varity_Form(request.POST)  # Ensure the correct form name is used
        if form.is_valid():
            chai_varty = form.cleaned_data['chai_var']  # Updated to match the correct field name
            stores = Store.objects.filter(chai_varieties=chai_varty)
        
    return render(request, 'chai/store_view.html', {'form': form, 'stores': stores})
