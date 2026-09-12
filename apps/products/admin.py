from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "order", "active")
    list_filter = ("status", "active")
    list_editable = ("order", "active")
    search_fields = ("name", "name_fa", "name_en")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Identity", {"fields": ("name", "name_fa", "name_ps", "name_en", "slug", "image", "status", "demo_url")}),
        ("Short", {"fields": ("short_description", "short_description_fa", "short_description_ps", "short_description_en")}),
        ("Full", {"fields": ("description", "description_fa", "description_ps", "description_en", "features")}),
        ("SEO", {"fields": ("seo_title", "seo_description")}),
        ("Display", {"fields": ("order", "active")}),
    )