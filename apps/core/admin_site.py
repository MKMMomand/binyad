from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class BinyadAdminSite(AdminSite):
    site_header = _("Binyad Control Panel")
    site_title = _("Binyad Admin")
    index_title = _("Dashboard")
    index_template = "admin/index.html"

    APP_ORDER = ["core", "contact", "services", "products", "portfolio", "blog", "pages"]

    def each_context(self, request):
        ctx = super().each_context(request)
        if request.user.is_authenticated:
            from apps.contact.models import ContactMessage, ConsultationRequest
            from apps.blog.models import Post
            from apps.services.models import Service
            from apps.products.models import Product
            from apps.portfolio.models import PortfolioProject

            ctx["stats"] = {
                "new_leads": ContactMessage.objects.filter(status="new").count(),
                "new_consultations": ConsultationRequest.objects.filter(status="new").count(),
                "published_posts": Post.objects.filter(status="published").count(),
                "services": Service.objects.filter(active=True).count(),
                "products": Product.objects.filter(active=True).count(),
                "projects": PortfolioProject.objects.filter(published=True).count(),
            }
        return ctx

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        app_list.sort(
            key=lambda a: self.APP_ORDER.index(a["app_label"])
            if a["app_label"] in self.APP_ORDER else 999
        )
        return app_list