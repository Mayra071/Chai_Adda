from django.urls import path
from . import views
app_name = "contacts"


urlpatterns = [
    # localhost:80001/chai
    path('', views.contact, name='contact'),
]
