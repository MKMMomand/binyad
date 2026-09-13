from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView, RedirectView

from apps.core.sitemaps import sitemaps
from apps.core.admin_site import BinyadAdminSite


# ---------------------------------------------------------------------------
# Brand the admin site (must run before urlpatterns is evaluated)
# ---------------------------------------------------------------------------
admin.site.__class__ = BinyadAdminSite
admin.site.site_header = "Binyad Control Panel"
admin.site.site_title = "Binyad Admin"
admin.site.index_title = "Dashboard"


# ---------------------------------------------------------------------------
# Non-i18n URLs (language-neutral) — admin, control panel, SEO, redirect
# ---------------------------------------------------------------------------
urlpatterns = [
    # Django admin (fallback / advanced)
    path(settings.ADMIN_URL, admin.site.urls),

    # 👇 Custom control panel — language-neutral, OUTSIDE i18n_patterns
    path("control/", include(("apps.dashboard.urls", "dashboard"), namespace="dashboard")),

    # Django's i18n language switcher
    path("i18n/", include("django.conf.urls.i18n")),

    # SEO
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),

    # Root redirect → default language. MUST be last.
    path("", RedirectView.as_view(url="/en/", permanent=False), name="root"),
]


# ---------------------------------------------------------------------------
# i18n-prefixed URLs (public site only) — /en/, /fa/, /ps/…
# ---------------------------------------------------------------------------
urlpatterns += i18n_patterns(
    path("", include(("apps.pages.urls", "pages"), namespace="pages")),
    path("services/",  include(("apps.services.urls",  "services"),  namespace="services")),
    path("products/",  include(("apps.products.urls",  "products"),  namespace="products")),
    path("portfolio/", include(("apps.portfolio.urls", "portfolio"), namespace="portfolio")),
    path("blog/",      include(("apps.blog.urls",      "blog"),      namespace="blog")),
    path("contact/",   include(("apps.contact.urls",   "contact"),   namespace="contact")),
    prefix_default_language=True,
)


# ---------------------------------------------------------------------------
# Media files in dev
# ---------------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
# handler403 = "apps.pages.views.error_403"
# handler404 = "apps.pages.views.error_404"
# handler500 = "apps.pages.views.error_500"