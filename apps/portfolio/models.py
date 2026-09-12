from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class PortfolioProject(TimeStampedModel):
    title = models.CharField(max_length=160)
    title_fa = models.CharField(max_length=160, blank=True)
    title_ps = models.CharField(max_length=160, blank=True)
    title_en = models.CharField(max_length=160, blank=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    client_name = models.CharField(max_length=160, blank=True)
    industry = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    description_fa = models.TextField(blank=True)
    description_ps = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    technologies = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="portfolio/", blank=True)
    completion_date = models.DateField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    is_demo = models.BooleanField(default=False, help_text="Marks this entry as a demo/sample, not real client work")

    class Meta:
        ordering = ["-completion_date", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_en or self.title) or "project"
            slug, i = base, 1
            while PortfolioProject.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:detail", kwargs={"slug": self.slug})

    def localized_title(self, lang):
        return getattr(self, f"title_{lang}") or self.title_en or self.title

    def localized_description(self, lang):
        return getattr(self, f"description_{lang}") or self.description_en or self.description

    def __str__(self):
        return self.title


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(PortfolioProject, related_name="gallery", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="portfolio/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["order", "id"]