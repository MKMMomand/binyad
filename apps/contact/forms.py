from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage, ConsultationRequest


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["full_name", "phone", "email", "company", "subject", "service", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "phone": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "service": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5, "required": True}),
        }

    def clean_full_name(self):
        v = self.cleaned_data["full_name"].strip()
        if len(v) < 2:
            raise forms.ValidationError(_("Please enter your full name."))
        return v


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = [
            "name", "phone", "email", "company", "business_type",
            "required_service", "project_description", "budget_range",
            "preferred_contact_method", "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "phone": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "business_type": forms.TextInput(attrs={"class": "form-control"}),
            "required_service": forms.TextInput(attrs={"class": "form-control"}),
            "project_description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "required": True}),
            "budget_range": forms.TextInput(attrs={"class": "form-control"}),
            "preferred_contact_method": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }