from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import PortfolioProject, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "thumb", "caption", "order")
    readonly_fields = ("thumb",)
    ordering = ("order",)

    @admin.display(description=_("Preview"))
    def thumb(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" class="admin-thumb" alt="">', obj.image.url)
        return "—"


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title_en", "client_name", "industry",
                    "featured", "published", "completion_date")
    list_display_links = ("title_en",)
    list_editable = ("featured", "published")
    list_filter = ("published", "featured", "is_demo", "industry")
    search_fields = ("title_en", "title_fa", "client_name", "description_en")
    prepopulated_fields = {"slug": ("title_en",)}
    date_hierarchy = "completion_date"
    inlines = [ProjectImageInline]
    save_on_top = True

    fieldsets = (
        (_("Identity"), {
            "fields": ("slug", "client_name", "industry", "completion_date"),
        }),
        (_("Titles"), {
            "fields": (("title_en", "title_fa", "title_ps"),),
            "classes": ("bilingual-group",),
        }),
        (_("Descriptions"), {
            "fields": ("description_en", "description_fa", "description_ps"),
            "classes": ("bilingual-group",),
        }),
        (_("Technologies"), {
            "fields": ("technologies",),
        }),
        (_("Media"), {
            "fields": ("image", "image_preview"),
        }),
        (_("Publishing"), {
            "fields": ("featured", "published", "is_demo"),
        }),
    )
    readonly_fields = ("image_preview",)

    @admin.display(description=_("Cover"))
    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="admin-thumb" alt="">', obj.image.url)
        return "—"

    @admin.display(description=_("Preview"))
    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" class="admin-thumb-lg" alt="">', obj.image.url)
        return _("No cover image.")