from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView, RedirectView

from apps.core.sitemaps import sitemaps


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain"
    ), name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("binyad-admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/en/", permanent=False), name="root"),
]

urlpatterns += i18n_patterns(
    path("", include(("apps.pages.urls", "pages"), namespace="pages")),
    path("services/", include(("apps.services.urls", "services"), namespace="services")),
    path("products/", include(("apps.products.urls", "products"), namespace="products")),
    path("portfolio/", include(("apps.portfolio.urls", "portfolio"), namespace="portfolio")),
    path("blog/", include(("apps.blog.urls", "blog"), namespace="blog")),
    path("contact/", include(("apps.contact.urls", "contact"), namespace="contact")),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "apps.pages.views.error_404"
handler403 = "apps.pages.views.error_403"
handler500 = "apps.pages.views.error_500"