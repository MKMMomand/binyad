from django import template
from django.conf import settings
from django.urls import translate_url
from django.utils.translation import get_language

register = template.Library()


@register.simple_tag(takes_context=True)
def switch_lang_url(context, target_lang):
    """
    Return the URL of the current page in the target language.
    Falls back to prefix-swapping if translate_url fails.
    """
    request = context["request"]
    current_path = request.get_full_path()

    try:
        return translate_url(current_path, target_lang)
    except Exception:
        # Manual fallback: strip current lang prefix and prepend target
        langs = [code for code, _ in settings.LANGUAGES]
        parts = current_path.strip("/").split("/", 1)
        if parts and parts[0] in langs:
            tail = parts[1] if len(parts) > 1 else ""
            return f"/{target_lang}/{tail}"
        return f"/{target_lang}/"