from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "name_fa", "order", "active")
    list_editable = ("order", "active")
    list_filter = ("active",)
    search_fields = ("name", "name_fa", "name_en")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Identity", {"fields": ("name", "name_fa", "name_ps", "name_en", "slug", "icon", "image")}),
        ("Short", {"fields": ("short_description", "short_description_fa", "short_description_ps", "short_description_en")}),
        ("Full", {"fields": ("description", "description_fa", "description_ps", "description_en", "features")}),
        ("SEO", {"fields": ("seo_title", "seo_description")}),
        ("Display", {"fields": ("order", "active")}),
    )