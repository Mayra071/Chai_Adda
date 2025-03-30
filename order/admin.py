from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'chai', 'customer_name', 'quantity', 'total_price', 'payment_status', 'ordered_at')
    list_filter = ('payment_status', 'sugar_level', 'chai__chai_type', 'ordered_at')
    search_fields = ('customer_name', 'chai__name', 'notes')
    readonly_fields = ('ordered_at', 'updated_at')
    date_hierarchy = 'ordered_at'
    raw_id_fields = ('user', 'chai', 'payment')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('chai', 'payment', 'user')