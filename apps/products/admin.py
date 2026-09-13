from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Product


STATUS_COLORS = {
    "planned":   "#8A6B2E",
    "dev":       "#2E8B57",
    "available": "#176B45",
    "custom":    "#4A5A8C",
}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name_en", "name_fa", "status_badge", "order", "active")
    list_display_links = ("name_en",)
    list_editable = ("order", "active")
    list_filter = ("active", "status")
    search_fields = ("name_en", "name_fa", "name_ps", "short_description_en", "description_en")
    prepopulated_fields = {"slug": ("name_en",)}
    ordering = ("order", "name_en")
    save_on_top = True

    fieldsets = (
        (_("Identity"), {
            "fields": ("slug", "status", "demo_url", ("order", "active")),
        }),
        (_("Names"), {
            "fields": (("name_en", "name_fa", "name_ps"),),
            "classes": ("bilingual-group",),
        }),
        (_("Short description"), {
            "fields": ("short_description_en", "short_description_fa", "short_description_ps"),
            "classes": ("bilingual-group",),
        }),
        (_("Full description"), {
            "fields": ("description_en", "description_fa", "description_ps"),
            "classes": ("bilingual-group",),
        }),
        (_("Features & media"), {
            "fields": ("features", "image", "image_preview"),
        }),
        (_("SEO"), {
            "fields": ("seo_title", "seo_description"),
            "classes": ("collapse",),
        }),
    )
    readonly_fields = ("image_preview",)

    @admin.display(description=_("Image"))
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="admin-thumb" alt="">', obj.image.url)
        return "—"

    @admin.display(description=_("Status"))
    def status_badge(self, obj):
        color = STATUS_COLORS.get(obj.status, "#666")
        return format_html(
            '<span style="display:inline-block;padding:3px 10px;border-radius:999px;'
            'background:{};color:#fff;font-size:12px;font-weight:600;">{}</span>',
            color, obj.get_status_display(),
        )

    @admin.display(description=_("Preview"))
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" class="admin-thumb-lg" alt="">', obj.image.url)
        return _("No image uploaded.")