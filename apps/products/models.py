from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel


class Product(TimeStampedModel):
    class Status(models.TextChoices):
        PLANNED = "planned", _("Planned")
        IN_DEVELOPMENT = "dev", _("In Development")
        AVAILABLE = "available", _("Available")
        CUSTOM = "custom", _("Custom")

    name = models.CharField(max_length=120)
    name_fa = models.CharField(max_length=120, blank=True)
    name_ps = models.CharField(max_length=120, blank=True)
    name_en = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    short_description_fa = models.CharField(max_length=255, blank=True)
    short_description_ps = models.CharField(max_length=255, blank=True)
    short_description_en = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    description_fa = models.TextField(blank=True)
    description_ps = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text="One feature per line")
    image = models.ImageField(upload_to="products/", blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    demo_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    seo_title = models.CharField(max_length=160, blank=True)
    seo_description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name_en or self.name) or "product"
            slug, i = base, 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    def features_list(self):
        return [line.strip() for line in (self.features or "").splitlines() if line.strip()]

    def localized_name(self, lang):
        return getattr(self, f"name_{lang}") or self.name_en or self.name

    def localized_description(self, lang):
        return getattr(self, f"description_{lang}") or self.description_en or self.description

    def __str__(self):
        return self.name