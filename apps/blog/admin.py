from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "post_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description=_("Posts"))
    def post_count(self, obj):
        return obj.posts.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "post_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description=_("Posts"))
    def post_count(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("thumb", "title", "category", "author",
                    "status", "published_at")
    list_display_links = ("title",)
    list_filter = ("status", "category", "author", "published_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    date_hierarchy = "published_at"
    save_on_top = True
    actions = ("make_published", "make_draft")

    fieldsets = (
        (_("Meta"), {
            "fields": ("slug", "author", "category", "tags",
                       "status", "published_at"),
        }),
        (_("Content"), {
            "fields": ("title", "excerpt", "content"),
        }),
        (_("Media"), {
            "fields": ("featured_image", "featured_preview"),
        }),
        (_("SEO"), {
            "fields": ("seo_title", "seo_description"),
            "classes": ("collapse",),
        }),
    )
    readonly_fields = ("featured_preview",)

    @admin.display(description=_("Image"))
    def thumb(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" class="admin-thumb" alt="">', obj.featured_image.url)
        return "—"

    @admin.display(description=_("Preview"))
    def featured_preview(self, obj):
        if obj and obj.featured_image:
            return format_html('<img src="{}" class="admin-thumb-lg" alt="">', obj.featured_image.url)
        return _("No image.")

    @admin.action(description=_("Publish selected posts"))
    def make_published(self, request, queryset):
        n = queryset.update(status="published")
        self.message_user(request, _("%d post(s) published.") % n)

    @admin.action(description=_("Move selected posts to draft"))
    def make_draft(self, request, queryset):
        n = queryset.update(status="draft")
        self.message_user(request, _("%d post(s) moved to draft.") % n)