from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("faq/", views.faq_view, name="faq"),
    path("mentions-legales/", views.mentions_legales_view, name="mentions_legales"),
    path("politique-de-confidentialite/", views.politique_confidentialite_view, name="politique_confidentialite"),
]
