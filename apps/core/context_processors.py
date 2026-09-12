from .models import SiteSettings, NavItem, SocialLink


def site_settings(request):
    try:
        return {
            "site": SiteSettings.load(),
            "nav_items": NavItem.objects.filter(active=True),
            "social_links": SocialLink.objects.filter(active=True),
        }
    except Exception:
        return {"site": None, "nav_items": [], "social_links": []}