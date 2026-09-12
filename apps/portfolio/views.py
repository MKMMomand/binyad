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