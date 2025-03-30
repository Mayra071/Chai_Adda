from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('options/<int:order_id>/', views.payment_options, name='payment_options'),
    path('gateway/<int:payment_id>/', views.payment_gateway, name='payment_gateway'),
    path('success/', views.payment_success, name='payment_success'),
]
