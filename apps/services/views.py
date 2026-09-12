from django.views.generic import ListView, DetailView
from django.utils.translation import get_language
from .models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"
    queryset = Service.objects.filter(active=True)


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "service"
    queryset = Service.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["related"] = Service.objects.filter(active=True).exclude(pk=self.object.pk)[:3]
        return ctx