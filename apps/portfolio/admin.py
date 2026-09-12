from django.contrib import admin
from .models import PortfolioProject, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "industry", "featured", "published", "is_demo", "completion_date")
    list_filter = ("published", "featured", "is_demo", "industry")
    search_fields = ("title", "client_name", "industry")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]