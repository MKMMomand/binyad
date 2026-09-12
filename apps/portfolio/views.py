from django.views.generic import ListView, DetailView
from .models import PortfolioProject


class PortfolioListView(ListView):
    model = PortfolioProject
    template_name = "portfolio/list.html"
    context_object_name = "projects"
    queryset = PortfolioProject.objects.filter(published=True)


class PortfolioDetailView(DetailView):
    model = PortfolioProject
    template_name = "portfolio/detail.html"
    context_object_name = "project"
    queryset = PortfolioProject.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        related = PortfolioProject.objects.filter(
            published=True, industry=self.object.industry,
        ).exclude(pk=self.object.pk)[:3]
        if not related:
            related = PortfolioProject.objects.filter(
                published=True,
            ).exclude(pk=self.object.pk)[:3]
        ctx["related_projects"] = related
        return ctx