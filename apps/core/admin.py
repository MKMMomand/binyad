from django.contrib import admin
from .models import SiteSettings, SocialLink, NavItem, FAQ, Testimonial, TeamMember

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("company_name", "name_fa", "name_ps", "name_en",
                                 "tagline_fa", "tagline_ps", "tagline_en", "logo", "favicon")}),
        ("Contact", {"fields": ("phone", "whatsapp", "email",
                                "address_fa", "address_ps", "address_en", "google_maps_url")}),
        ("Social", {"fields": ("facebook", "instagram", "linkedin", "telegram")}),
        ("Hours", {"fields": ("opening_hours_fa", "opening_hours_ps", "opening_hours_en")}),
        ("Footer", {"fields": ("footer_text_fa", "footer_text_ps", "footer_text_en")}),
    )

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order", "active")
    list_editable = ("order", "active")
    search_fields = ("name",)

@admin.register(NavItem)
class NavItemAdmin(admin.ModelAdmin):
    list_display = ("label_fa", "label_en", "url_name", "order", "active")
    list_editable = ("order", "active")

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "language", "category", "order", "active")
    list_filter = ("language", "category", "active")
    search_fields = ("question", "answer")

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "order", "active")
    list_editable = ("order", "active")

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "position_en", "order", "active")
    list_editable = ("order", "active")