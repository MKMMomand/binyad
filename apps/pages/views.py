from django.shortcuts import redirect
from django.views.generic import TemplateView
from apps.services.models import Service
from apps.products.models import Product
from apps.portfolio.models import PortfolioProject
from apps.blog.models import Post
from apps.core.models import FAQ, Testimonial


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["services"] = Service.objects.filter(active=True)[:8]
        ctx["flagship"] = Product.objects.filter(active=True, slug="binyad-office").first() \
                          or Product.objects.filter(active=True).first()
        ctx["testimonials"] = Testimonial.objects.filter(active=True)[:6]
        ctx["faqs"] = FAQ.objects.filter(active=True)[:6]
        return ctx


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ServicesOverviewView(TemplateView):
    template_name = "pages/services_overview.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["services"] = Service.objects.filter(active=True)
        return ctx


class ProductsOverviewView(TemplateView):
    template_name = "pages/products_overview.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["products"] = Product.objects.filter(active=True)
        return ctx


class PortfolioOverviewView(TemplateView):
    template_name = "pages/portfolio_overview.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["projects"] = PortfolioProject.objects.filter(published=True)
        return ctx


class BlogOverviewView(TemplateView):
    template_name = "pages/blog_overview.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["posts"] = Post.objects.filter(status=Post.Status.PUBLISHED)[:9]
        return ctx


class SolutionsView(TemplateView):
    template_name = "pages/solutions.html"


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"


class TermsView(TemplateView):
    template_name = "pages/terms.html"


class ContactRedirectView(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect("contact:contact")


class ConsultationRedirectView(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect("contact:consultation")


def error_404(request, exception=None):
    return TemplateView.as_view(template_name="errors/404.html")(request)


def error_403(request, exception=None):
    return TemplateView.as_view(template_name="errors/403.html")(request)


def error_500(request):
    return TemplateView.as_view(template_name="errors/500.html")(request)