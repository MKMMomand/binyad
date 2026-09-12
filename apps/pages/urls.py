# from django.urls import path
# from django.views.generic import RedirectView
# from . import views
# app_name = "pages"
# urlpatterns = [
#     path("", views.HomeView.as_view(), name="home"),
#     path("about/", views.AboutView.as_view(), name="about"),
#     path("solutions/", views.SolutionsView.as_view(), name="solutions"),
#     path("services/", RedirectView.as_view(pattern_name="services:list", permanent=False), name="services_list"),
#     path("products/", RedirectView.as_view(pattern_name="products:list", permanent=False), name="products_list"),
#     path("portfolio/", RedirectView.as_view(pattern_name="portfolio:list", permanent=False), name="portfolio_list"),
#     path("blog/", RedirectView.as_view(pattern_name="blog:list", permanent=False), name="blog_list"),
#     path("contact/", RedirectView.as_view(pattern_name="contact:contact", permanent=False), name="contact"),
#     path("consultation/", RedirectView.as_view(pattern_name="contact:consultation", permanent=False), name="consultation"),
#     path("privacy/", views.PrivacyView.as_view(), name="privacy"),
#     path("terms/", views.TermsView.as_view(), name="terms"),
# ]


from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("solutions/", views.SolutionsView.as_view(), name="solutions"),
    path("privacy/", views.PrivacyView.as_view(), name="privacy"),
    path("terms/", views.TermsView.as_view(), name="terms"),
]