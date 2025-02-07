from django.contrib import admin
from .models import Chai_varity, ChaiReview, Store

class ChaiReviewInline(admin.TabularInline):
    model = ChaiReview
    extra = 1

class ChaiVarietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'Chai_type')  # Updated field name
    inlines = [ChaiReviewInline]

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    filter_horizontal = ('chai_varieties',)

admin.site.register(Chai_varity, ChaiVarietyAdmin)
admin.site.register(Store, StoreAdmin)
