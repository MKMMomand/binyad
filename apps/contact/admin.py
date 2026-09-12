from django.contrib import admin
from .models import ContactMessage, ConsultationRequest

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "subject", "service", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "phone", "email", "subject", "message")
    readonly_fields = ("created_at", "updated_at", "ip_address")
    fieldsets = (
        ("Contact info", {"fields": ("full_name", "phone", "email", "company")}),
        ("Message", {"fields": ("subject", "service", "message")}),
        ("Tracking", {"fields": ("status", "internal_notes", "ip_address", "created_at", "updated_at")}),
    )

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "required_service", "business_type", "status", "created_at")
    list_filter = ("status", "preferred_contact_method", "created_at")
    search_fields = ("name", "phone", "email", "project_description")
    readonly_fields = ("created_at", "updated_at", "ip_address")
    fieldsets = (
        ("Contact info", {"fields": ("name", "phone", "email", "company")}),
        ("Project", {"fields": ("business_type", "required_service", "project_description", "budget_range", "preferred_contact_method", "message")}),
        ("Tracking", {"fields": ("status", "internal_notes", "ip_address", "created_at", "updated_at")}),
    )