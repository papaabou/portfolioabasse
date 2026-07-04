from django.db import models
from projects.models import Project
from client.models import Client
from django.utils import timezone
from core.models import SeoMixin

class Testimonial(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="testimonials")
    
    name = models.CharField(max_length=140)
    role = models.CharField(max_length=140, blank=True)
    company = models.CharField(max_length=140, blank=True)
    body = models.TextField()
    email = models.EmailField(blank=True)

    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(i, f"{i} Stars") for i in range(1, 6)],
        help_text="Rating out of 5",
    )
    
    featured = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-featured", "order"]

    def __str__(self):
        return f"{self.name} — {self.company or ''}"

class TestimonialPageSettings(SeoMixin, models.Model):
    """
    Singleton model to store dynamic text for testimonial pages.
    """
    # Submission page
    submit_heading = models.CharField(max_length=200, default="Partagez votre expérience")
    submit_subheading = models.TextField(default="Votre avis compte énormément. Merci d'avoir fait confiance à Abasse NIANG pour votre projet !")

    # Thank you page
    thanks_title = models.CharField(max_length=200, default="Merci pour votre témoignage")
    thanks_subheading = models.CharField(max_length=200, default="Témoignage reçu")
    thanks_message = models.TextField(default="Votre témoignage a bien été reçu et sera publié sur le site après validation.")
    
    def __str__(self):
        return "Testimonial Page Settings"

    class Meta:
        verbose_name = "Testimonial Page Settings"
        verbose_name_plural = "Testimonial Page Settings"
