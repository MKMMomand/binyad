from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class SiteSettings(models.Model):
    company_name = models.CharField(max_length=120, default="Binyad")
    name_fa = models.CharField(max_length=120, default="بنیاد")
    name_ps = models.CharField(max_length=120, default="بنیاد")
    name_en = models.CharField(max_length=120, default="Binyad")
    tagline_fa = models.CharField(max_length=255, default="راه‌حل‌های مدیریت، اداری و تکنالوژی")
    tagline_ps = models.CharField(max_length=255, blank=True)
    tagline_en = models.CharField(max_length=255, default="Business, Management & IT Solutions")
    logo = models.ImageField(upload_to="brand/", blank=True, validators=[FileExtensionValidator(["png","jpg","jpeg","svg","webp"])])
    favicon = models.ImageField(upload_to="brand/", blank=True)
    phone = models.CharField(max_length=40, blank=True)
    whatsapp = models.CharField(max_length=40, blank=True, help_text="International format without +, e.g. 93700000000")
    email = models.EmailField(blank=True)
    address_fa = models.CharField(max_length=255, blank=True)
    address_ps = models.CharField(max_length=255, blank=True)
    address_en = models.CharField(max_length=255, blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    opening_hours_fa = models.CharField(max_length=255, blank=True)
    opening_hours_ps = models.CharField(max_length=255, blank=True)
    opening_hours_en = models.CharField(max_length=255, blank=True)
    google_maps_url = models.URLField(blank=True)
    footer_text_fa = models.TextField(blank=True)
    footer_text_ps = models.TextField(blank=True)
    footer_text_en = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SocialLink(TimeStampedModel):
    name = models.CharField(max_length=60)
    url = models.URLField()
    icon = models.CharField(max_length=60, blank=True, help_text="CSS icon class")
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ["order", "name"]
    def __str__(self):
        return self.name


class NavItem(TimeStampedModel):
    label_fa = models.CharField(max_length=60)
    label_ps = models.CharField(max_length=60, blank=True)
    label_en = models.CharField(max_length=60, blank=True)
    url_name = models.CharField(max_length=120, help_text="Django URL name e.g. pages:home")
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ["order"]
    def __str__(self):
        return self.label_fa or self.label_en


class FAQ(TimeStampedModel):
    class Language(models.TextChoices):
        FA = "fa", _("Dari/Persian")
        PS = "ps", _("Pashto")
        EN = "en", _("English")

    question = models.CharField(max_length=255)
    answer = models.TextField()
    language = models.CharField(max_length=2, choices=Language.choices, default=Language.FA)
    category = models.CharField(max_length=60, blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
    def __str__(self):
        return self.question[:80]


class Testimonial(TimeStampedModel):
    name = models.CharField(max_length=120)
    company = models.CharField(max_length=120, blank=True)
    position = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    image = models.ImageField(upload_to="testimonials/", blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ["order", "-created_at"]
    def __str__(self):
        return self.name


class TeamMember(TimeStampedModel):
    name = models.CharField(max_length=120)
    position_fa = models.CharField(max_length=120, blank=True)
    position_ps = models.CharField(max_length=120, blank=True)
    position_en = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ["order"]
    def __str__(self):
        return self.name