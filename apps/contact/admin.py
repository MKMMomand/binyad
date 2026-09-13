from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage, ConsultationRequest


STATUS_COLORS = {
    "new":         "#176B45",
    "contacted":   "#2E8B57",
    "in_progress": "#C2872B",
    "completed":   "#3B7A57",
    "cancelled":   "#9B3A3A",
}


class BaseLeadAdmin(admin.ModelAdmin):
    save_on_top = True
    list_per_page = 30
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at", "ip_address", "status_badge")
    ordering = ("-created_at",)

    @admin.display(description=_("Status"))
    def status_badge(self, obj):
        color = STATUS_COLORS.get(obj.status, "#666")
        return format_html(
            '<span style="display:inline-block;padding:3px 10px;border-radius:999px;'
            'background:{};color:#fff;font-size:12px;font-weight:600;">{}</span>',
            color, obj.get_status_display(),
        )

    @admin.display(description=_("Status"))
    def status_pill(self, obj):
        return self.status_badge(obj)


@admin.register(ContactMessage)
class ContactMessageAdmin(BaseLeadAdmin):
    list_display = ("full_name", "email", "phone", "company",
                    "subject", "status", "status_pill", "created_at")
    #                                           ^^^^^^  <-- add this
    list_display_links = ("full_name",)
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email", "phone", "company", "subject", "message")
    actions = ("mark_contacted", "mark_completed")

    fieldsets = (
        (_("Lead"), {
            "fields": ("full_name", ("email", "phone"), "company",
                       "subject", "service", "status", "status_badge"),
        }),
        (_("Message"), {"fields": ("message",)}),
        (_("Internal"), {
            "fields": ("internal_notes",),
            "classes": ("collapse",),
        }),
        (_("Metadata"), {
            "fields": ("created_at", "updated_at", "ip_address"),
            "classes": ("collapse",),
        }),
    )

    @admin.action(description=_("Mark as contacted"))
    def mark_contacted(self, request, queryset):
        n = queryset.update(status="contacted")
        self.message_user(request, _("%d lead(s) marked as contacted.") % n)

    @admin.action(description=_("Mark as completed"))
    def mark_completed(self, request, queryset):
        n = queryset.update(status="completed")
        self.message_user(request, _("%d lead(s) completed.") % n)


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(BaseLeadAdmin):
    list_display = ("name", "company", "email", "phone",
                    "business_type", "status", "status_pill", "created_at")
    #                                 ^^^^^^  <-- add this
    list_display_links = ("name",)
    list_editable = ("status",)
    list_filter = ("status", "business_type", "preferred_contact_method", "created_at")
    search_fields = ("name", "company", "email", "phone", "project_description")
    actions = ("mark_contacted", "mark_completed")

    fieldsets = (
        (_("Lead"), {
            "fields": ("name", ("email", "phone"), "company",
                       "business_type", "required_service",
                       "preferred_contact_method", "status", "status_badge"),
        }),
        (_("Project"), {
            "fields": ("project_description", "budget_range", "message"),
        }),
        (_("Internal"), {
            "fields": ("internal_notes",),
            "classes": ("collapse",),
        }),
        (_("Metadata"), {
            "fields": ("created_at", "updated_at", "ip_address"),
            "classes": ("collapse",),
        }),
    )

    @admin.action(description=_("Mark as contacted"))
    def mark_contacted(self, request, queryset):
        n = queryset.update(status="contacted")
        self.message_user(request, _("%d lead(s) marked as contacted.") % n)

    @admin.action(description=_("Mark as completed"))
    def mark_completed(self, request, queryset):
        n = queryset.update(status="completed")
        self.message_user(request, _("%d lead(s) completed.") % n)