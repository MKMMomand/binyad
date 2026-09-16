# sitemaps.py
from django.contrib.sitemaps import Sitemap
from apps.blog.models import Post
from apps.services.models import Service

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    def items(self): return Post.objects.filter(status=Post.Status.PUBLISHED)
    def lastmod(self, obj): return obj.published_at