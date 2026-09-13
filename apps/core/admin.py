from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    SiteSettings, SocialLink, NavItem, FAQ,
    Testimonial, TeamMember,
)


# ---------------------------------------------------------------------------
# Site Settings  (singleton — only one row, no add, no delete)
# ---------------------------------------------------------------------------
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("__str__", "phone", "email", "whatsapp")

    fieldsets = (
        (_("Company identity"), {
            "fields": (
                ("company_name",),
                ("name_fa", "name_ps", "name_en"),
                ("tagline_fa", "tagline_ps", "tagline_en"),
                ("logo", "logo_preview", "favicon", "favicon_preview"),
            ),
        }),
        (_("Contact details"), {
            "fields": ("phone", "whatsapp", "email", "google_maps_url"),
        }),
        (_("Address"), {
            "fields": ("address_fa", "address_ps", "address_en"),
        }),
        (_("Opening hours"), {
            "fields": ("opening_hours_fa", "opening_hours_ps", "opening_hours_en"),
        }),
        (_("Social links"), {
            "fields": ("facebook", "instagram", "linkedin", "telegram"),
        }),
        (_("Footer text"), {
            "fields": ("footer_text_fa", "footer_text_ps", "footer_text_en"),
        }),
    )
    readonly_fields = ("logo_preview", "favicon_preview")

    # --- singleton enforcement ---
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    # --- previews ---
    @admin.display(description=_("Current logo"))
    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html('<img src="{}" class="admin-thumb-lg" alt="">', obj.logo.url)
        return _("No logo uploaded.")

    @admin.display(description=_("Current favicon"))
    def favicon_preview(self, obj):
        if obj and obj.favicon:
            return format_html('<img src="{}" class="admin-thumb" alt="">', obj.favicon.url)
        return "—"


# ---------------------------------------------------------------------------
# Social links
# ---------------------------------------------------------------------------
@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "icon", "order", "active")
    list_display_links = ("name",)
    list_editable = ("order", "active")
    list_filter = ("active",)
    search_fields = ("name", "url")
    ordering = ("order", "name")


# ---------------------------------------------------------------------------
# Navigation items
# ---------------------------------------------------------------------------
@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = ("label_en", "label_fa", "label_ps", "url_name", "order", "active")
    list_display_links = ("label_en",)
    list_editable = ("order", "active")
    list_filter = ("active",)
    search_fields = ("label_en", "label_fa", "label_ps", "url_name")
    ordering = ("order",)


# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "language", "category", "order", "active")
    list_display_links = ("question",)
    list_editable = ("order", "active")
    list_filter = ("active", "language", "category")
    search_fields = ("question", "answer")
    ordering = ("order",)


# ---------------------------------------------------------------------------
# Testimonials
# ---------------------------------------------------------------------------
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "company", "position", "order", "active")
    list_display_links = ("name",)
    list_editable = ("order", "active")
    list_filter = ("active",)
    search_fields = ("name", "company", "message")
    ordering = ("order",)

    @admin.display(description=_("Photo"))
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="admin-thumb" alt="">', obj.image.url)
        return "—"


# ---------------------------------------------------------------------------
# Team members
# ---------------------------------------------------------------------------
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "position_en", "order", "active")
    list_display_links = ("name",)
    list_editable = ("order", "active")
    list_filter = ("active",)
    search_fields = ("name", "position_en", "bio")
    ordering = ("order",)

    fieldsets = (
        (_("Identity"), {
            "fields": ("name", ("position_en", "position_fa", "position_ps"), "photo", "photo_preview"),
        }),
        (_("Bio"), {"fields": ("bio",)}),
        (_("Display"), {"fields": ("order", "active")}),
    )
    readonly_fields = ("photo_preview",)

    @admin.display(description=_("Photo"))
    def thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" class="admin-thumb" alt="">', obj.photo.url)
        return "—"

    @admin.display(description=_("Preview"))
    def photo_preview(self, obj):
        if obj and obj.photo:
            return format_html('<img src="{}" class="admin-thumb-lg" alt="">', obj.photo.url)
        return "—"