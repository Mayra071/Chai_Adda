from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', include('contacts.urls', namespace='contact')),
    path('chai/', include('chai.urls', namespace='chai')),
    path('order/', include('order.urls')),
    path('payment/', include('payment.urls', namespace='payment')),
]

# 🔹 DEV ONLY
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
