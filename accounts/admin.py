from django.contrib import admin
from .models import UserProfile, ConsultationRequest


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'membership', 'is_verified', 'created_at']
    list_filter = ['membership', 'is_verified']
    search_fields = ['user__username', 'user__email', 'phone', 'company']
    list_editable = ['membership', 'is_verified']


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'subject', 'status', 'created_at']
    list_filter = ['status', 'subject']
    list_editable = ['status']
    search_fields = ['full_name', 'phone']
    ordering = ['-created_at']
