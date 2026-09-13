from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView

from apps.dashboard.mixins import StaffRequiredMixin
from apps.contact.models import ContactMessage, ConsultationRequest
from apps.blog.models import Post
from apps.services.models import Service
from apps.products.models import Product
from apps.portfolio.models import PortfolioProject
from apps.core.models import SiteSettings


# ---------------------------------------------------------------------------
# Login / Logout
# ---------------------------------------------------------------------------
def dashboard_login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff and user.is_active:
            login(request, user)
            return redirect(request.GET.get("next") or "dashboard:index")
        error = "Invalid credentials or insufficient permissions."
    return render(request, "dashboard/login.html", {"error": error})


def dashboard_logout(request):
    logout(request)
    return redirect("dashboard:login")


# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------
class OverviewView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Lead counts
        new_contacts = ContactMessage.objects.filter(status="new").count()
        new_consultations = ConsultationRequest.objects.filter(status="new").count()

        # Content counts
        ctx["stats"] = {
            "new_contacts": new_contacts,
            "new_consultations": new_consultations,
            "total_leads": ContactMessage.objects.count()
                            + ConsultationRequest.objects.count(),
            "published_posts": Post.objects.filter(status="published").count(),
            "services": Service.objects.filter(active=True).count(),
            "products": Product.objects.filter(active=True).count(),
            "projects": PortfolioProject.objects.filter(published=True).count(),
        }

        # Recent activity feed
        ctx["recent_contacts"] = ContactMessage.objects.order_by("-created_at")[:5]
        ctx["recent_consultations"] = ConsultationRequest.objects.order_by("-created_at")[:5]

        # Chart data — leads per day, last 14 days
        today = timezone.now().date()
        days = [today - timezone.timedelta(days=i) for i in range(13, -1, -1)]
        lead_series = []
        for d in days:
            c = ContactMessage.objects.filter(created_at__date=d).count()
            q = ConsultationRequest.objects.filter(created_at__date=d).count()
            lead_series.append({"date": d.strftime("%b %d"), "count": c + q})
        ctx["chart_labels"] = [x["date"] for x in lead_series]
        ctx["chart_values"] = [x["count"] for x in lead_series]

        return ctx


# ---------------------------------------------------------------------------
# Leads
# ---------------------------------------------------------------------------
class LeadsListView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/leads/list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["contacts"] = ContactMessage.objects.order_by("-created_at")[:50]
        ctx["consultations"] = ConsultationRequest.objects.order_by("-created_at")[:50]
        return ctx


class LeadDetailView(StaffRequiredMixin, DetailView):
    template_name = "dashboard/leads/detail.html"

    def get_object(self):
        kind = self.kwargs["kind"]
        pk = self.kwargs["pk"]
        if kind == "contact":
            return get_object_or_404(ContactMessage, pk=pk)
        if kind == "consultation":
            return get_object_or_404(ConsultationRequest, pk=pk)
        raise Http404

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        new_status = request.POST.get("status")
        notes = request.POST.get("internal_notes")
        if new_status:
            obj.status = new_status
        if notes is not None:
            obj.internal_notes = notes
        obj.save()
        return HttpResponseRedirect(request.path)


# ---------------------------------------------------------------------------
# Content browser (generic)
# ---------------------------------------------------------------------------
CONTENT_TYPES = {
    "services":   {"model": Service,          "title": "Services",   "icon": "🛠"},
    "products":   {"model": Product,          "title": "Products",   "icon": "📦"},
    "portfolio":  {"model": PortfolioProject, "title": "Portfolio",  "icon": "🎨"},
    "blog":       {"model": Post,             "title": "Blog Posts", "icon": "📝"},
    "faq":        {"model": None,             "title": "FAQ",        "icon": "❓"},
}


class ContentListView(StaffRequiredMixin, ListView):
    template_name = "dashboard/content/list.html"
    context_object_name = "items"
    paginate_by = 25

    def get_queryset(self):
        """
        Return a normalized list of dicts so the template never has to guess
        which attribute holds the display name.
        """
        key = self.kwargs["kind"]
        cfg = CONTENT_TYPES.get(key)

        if not cfg or cfg["model"] is None:
            return []

        Model = cfg["model"]
        rows = []

        for obj in Model.objects.all().order_by("-updated_at"):
            # Try common name/title attributes in order
            title = (
                getattr(obj, "name", None)
                or getattr(obj, "title", None)
                or getattr(obj, "question", None)   # FAQ
                or getattr(obj, "full_name", None)  # ContactMessage
                or str(obj)
            )

            rows.append({
                "obj": obj,
                "title": title,
                "updated_at": getattr(obj, "updated_at", None),
                "is_active": getattr(obj, "active", None),
                "status": getattr(obj, "status", None),
                "admin_url": f"/binyad-admin/{Model._meta.app_label}/"
                             f"{Model._meta.model_name}/{obj.pk}/change/",
            })

        return rows

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        key = self.kwargs["kind"]
        ctx["kind"] = key
        ctx["config"] = CONTENT_TYPES.get(key, {})
        return ctx
# ---------------------------------------------------------------------------
# Site Settings
# ---------------------------------------------------------------------------
class SettingsView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/settings.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["site"] = SiteSettings.objects.first()
        return ctx