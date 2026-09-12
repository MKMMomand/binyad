from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.services.models import Service
from apps.products.models import Product
from apps.blog.models import Post

class StaticSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"
    def items(self):
        return ["pages:home", "pages:about", "pages:services_list",
                "pages:products_list", "pages:portfolio_list", "pages:blog_list",
                "pages:contact", "pages:consultation", "pages:privacy", "pages:terms"]
    def location(self, item):
        return reverse(item)

class ServiceSitemap(Sitemap):
    priority = 0.8
    def items(self): return Service.objects.filter(active=True)
    def location(self, obj): return obj.get_absolute_url()
    def lastmod(self, obj): return obj.updated_at

class ProductSitemap(Sitemap):
    priority = 0.7
    def items(self): return Product.objects.filter(active=True)
    def location(self, obj): return obj.get_absolute_url()
    def lastmod(self, obj): return obj.updated_at

class PostSitemap(Sitemap):
    priority = 0.6
    def items(self): return Post.objects.filter(status=Post.Status.PUBLISHED)
    def location(self, obj): return obj.get_absolute_url()
    def lastmod(self, obj): return obj.updated_at

sitemaps = {
    "static": StaticSitemap,
    "services": ServiceSitemap,
    "products": ProductSitemap,
    "blog": PostSitemap,
}