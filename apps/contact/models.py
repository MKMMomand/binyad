from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class ContactMessage(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", _("New")
        CONTACTED = "contacted", _("Contacted")
        IN_PROGRESS = "progress", _("In Progress")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled", _("Cancelled")

    full_name = models.CharField(max_length=140)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=140, blank=True)
    subject = models.CharField(max_length=200)
    service = models.CharField(max_length=140, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    internal_notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.subject}"


class ConsultationRequest(TimeStampedModel):
    class Status(models.TextChoices):
        NEW = "new", _("New")
        CONTACTED = "contacted", _("Contacted")
        IN_PROGRESS = "progress", _("In Progress")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled", _("Cancelled")

    class ContactMethod(models.TextChoices):
        PHONE = "phone", _("Phone")
        WHATSAPP = "whatsapp", _("WhatsApp")
        EMAIL = "email", _("Email")

    name = models.CharField(max_length=140)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=140, blank=True)
    business_type = models.CharField(max_length=140, blank=True)
    required_service = models.CharField(max_length=140, blank=True)
    project_description = models.TextField()
    budget_range = models.CharField(max_length=80, blank=True)
    preferred_contact_method = models.CharField(max_length=20, choices=ContactMethod.choices, default=ContactMethod.PHONE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    internal_notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.required_service or self.business_type}"