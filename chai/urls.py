from django.urls import path
from . import views

app_name = "chai"

urlpatterns = [
    # localhost:80001/chai
    path('', views.all_chai, name='all_chai'),
    # localhost:80001/chai/chai_detail
    path('chai/<int:chai_id>/', views.chai_detail, name='chai_detail'),
    path('order/<int:chai_id>/', views.order_chai, name='order_chai'),
    path('stores/', views.store_view, name='stores'),
]
