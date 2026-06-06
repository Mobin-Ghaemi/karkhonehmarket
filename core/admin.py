from django.contrib import admin
from .models import Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'location', 'price', 'is_featured', 'created_at']
    list_filter = ['category', 'status', 'is_featured']
    search_fields = ['title', 'location', 'description']
    list_editable = ['is_featured']
