from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .forms import ContactForm, ConsultationForm


def _client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    return xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR")


def _notify(subject, body):
    recipient = settings.CONTACT_NOTIFICATION_EMAIL
    if not recipient:
        return
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=True)
    except Exception:
        pass


class ContactView(TemplateView):
    template_name = "contact/contact.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault("form", ContactForm())
        return ctx

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.ip_address = _client_ip(request)
            obj.save()
            _notify(
                f"[Contact] {obj.subject}",
                f"From: {obj.full_name} <{obj.email}>\nPhone: {obj.phone}\nCompany: {obj.company}\nService: {obj.service}\n\n{obj.message}",
            )
            messages.success(request, _("Thank you. Your message was received."))
            return redirect("contact:contact")
        return render(request, self.template_name, {"form": form})


class ConsultationView(TemplateView):
    template_name = "contact/consultation.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault("form", ConsultationForm())
        return ctx

    def post(self, request, *args, **kwargs):
        form = ConsultationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.ip_address = _client_ip(request)
            obj.save()
            _notify(
                f"[Consultation] {obj.name}",
                f"From: {obj.name} <{obj.email}>\nPhone: {obj.phone}\nBusiness: {obj.business_type}\nService: {obj.required_service}\nBudget: {obj.budget_range}\n\n{obj.project_description}",
            )
            return redirect("contact:consultation_success")
        return render(request, self.template_name, {"form": form})


class ConsultationSuccessView(TemplateView):
    template_name = "contact/consultation_success.html"