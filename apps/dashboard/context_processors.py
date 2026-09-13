def dashboard_context(request):
    """Provides branding + unread counts to every dashboard template."""
    if not request.path.startswith("/control/"):
        return {}

    from apps.core.models import SiteSettings

    try:
        site = SiteSettings.objects.first()
    except Exception:
        site = None

    return {
        "site_settings": site,
        "dashboard_brand": "Binyad Control Panel",
    }