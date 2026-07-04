from django.urls import path
from . import views

urlpatterns = [
    path("", views.testimonials_list, name="testimonials_list"),
    path("submit/", views.testimonial_submit, name="testimonial_submit"),
    path("thanks/", views.testimonial_thanks, name="testimonial_thanks"),
]
