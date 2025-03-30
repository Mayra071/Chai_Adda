from django.contrib import admin
from .models import ChaiVariety, ChaiReview, Store

class ChaiReviewInline(admin.TabularInline):
    model = ChaiReview
    extra = 1
    readonly_fields = ('date_added',)

@admin.register(ChaiVariety)
class ChaiVarietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'chai_type', 'price')
    list_filter = ('chai_type',)
    search_fields = ('name', 'description')
    inlines = [ChaiReviewInline]

@admin.register(ChaiReview)
class ChaiReviewAdmin(admin.ModelAdmin):
    list_display = ('chai', 'user', 'rating', 'date_added')
    list_filter = ('rating', 'date_added')
    search_fields = ('user__username', 'comment')
    readonly_fields = ('date_added',)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active', 'is_currently_open')
    list_filter = ('is_active', 'location')
    search_fields = ('name', 'location', 'address')
    filter_horizontal = ('chai_varieties',)
    readonly_fields = ('created_at', 'updated_at')

    def is_currently_open(self, obj):
        return obj.is_open()
    is_currently_open.boolean = True
    is_currently_open.short_description = 'Currently Open'
