"""
Template tags for pulling language-specific fields off model instances.

Usage:
    {% load i18n_fields %}
    {% tfield service 'name' %}
    {% tfield product 'short_description' %}
"""
from django import template
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag
def tfield(obj, base):
    """
    Return obj.<base>_<lang> if it exists and is non-empty,
    otherwise fall back to obj.<base>.

    Example:
        tfield(service, 'name')
        -> service.name_fa  (if lang=fa and non-empty)
        -> service.name     (fallback)
    """
    if obj is None:
        return ""

    lang = (get_language() or "en").split("-")[0]

    if lang != "en":
        localized = getattr(obj, f"{base}_{lang}", None)
        if localized:
            return localized

    return getattr(obj, base, "") or ""


@register.filter
def tf(obj, base):
    """
    Filter version of tfield, usable inside {% blocktrans %}:
        {% blocktrans with svc_name=service|tf:"name" %}...{{ svc_name }}...{% endblocktrans %}
    """
    return tfield(obj, base)