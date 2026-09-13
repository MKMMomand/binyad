from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/",  views.dashboard_login,  name="login"),
    path("logout/", views.dashboard_logout, name="logout"),

    path("", views.OverviewView.as_view(), name="index"),

    path("leads/", views.LeadsListView.as_view(), name="leads"),
    path("leads/<str:kind>/<int:pk>/", views.LeadDetailView.as_view(), name="lead_detail"),

    path("content/<str:kind>/", views.ContentListView.as_view(), name="content_list"),

    path("settings/", views.SettingsView.as_view(), name="settings"),
]