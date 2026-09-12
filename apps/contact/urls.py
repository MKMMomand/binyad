from django.urls import path
from . import views
app_name = "contact"
urlpatterns = [
    path("", views.ContactView.as_view(), name="contact"),
    path("consultation/", views.ConsultationView.as_view(), name="consultation"),
    path("consultation/success/", views.ConsultationSuccessView.as_view(), name="consultation_success"),
]