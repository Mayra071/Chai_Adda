from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/<int:chai_id>/', views.create_order, name='create_order'),
    path('submit/', views.submit_order, name='submit_order'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('history/', views.order_history, name='order_history'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
]