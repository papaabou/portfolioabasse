from django.db import models
from projects.models import Project
from testimonials.models import Testimonial
from services.models import Service

class BNAboutPage(models.Model):
    # -----------------
    # HERO
    # -----------------
    hero_title = models.CharField(max_length=255)
    hero_subtitle = models.TextField(blank=True, null=True)
    hero_badge_text = models.CharField(max_length=100, blank=True)
    hero_video_url = models.URLField(blank=True, null=True)
    hero_cta_text = models.CharField(max_length=50, blank=True)
    hero_cta_link = models.URLField(blank=True, null=True)

    # -----------------
    # SERVICES
    # -----------------
    service_title = models.CharField(max_length=255)
    service_subtitle = models.TextField(blank=True, null=True)
    services = models.ManyToManyField(Service, blank=True)

    # -----------------
    # PROJECTS / PORTFOLIO
    # -----------------
    project_title = models.CharField(max_length=255)
    project_subtitle = models.TextField(blank=True, null=True)
    projects = models.ManyToManyField(Project, blank=True)

    # -----------------
    # PRICING / PACKAGES
    # -----------------
    pricing_title = models.CharField(max_length=255)
    pricing_subtitle = models.TextField(blank=True, null=True)

    # -----------------
    # EXPERIENCE
    # -----------------
    experience_title = models.CharField(max_length=255)
    experience_subtitle = models.TextField(blank=True, null=True)

    # -----------------
    # PROCESS
    # -----------------
    process_title = models.CharField(max_length=255)
    process_subtitle = models.TextField(blank=True, null=True)

    # -----------------
    # TESTIMONIALS
    # -----------------
    testimonial_title = models.CharField(max_length=255)
    testimonial_subtitle = models.TextField(blank=True, null=True)
    testimonials = models.ManyToManyField(Testimonial, blank=True)

    # -----------------
    # FAQ
    # -----------------
    faq_title = models.CharField(max_length=255)
    faq_subtitle = models.TextField(blank=True, null=True)

    # -----------------
    # MEETING / CONTACT
    # -----------------
    meeting_title = models.CharField(max_length=255)
    meeting_subtitle = models.TextField(blank=True, null=True)
    calendly_url = models.URLField(blank=True, null=True)

    contact_title = models.CharField(max_length=255)
    contact_subtitle = models.TextField(blank=True, null=True)

    # -----------------
    # SEO
    # -----------------
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "BN About Page"

class BNPricingPlan(models.Model):
    about_page = models.ForeignKey(
        BNAboutPage,
        on_delete=models.CASCADE,
        related_name="pricing_plans"
    )
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    features = models.TextField(help_text="One feature per line")
    featured = models.BooleanField(default=False)
    cta_text = models.CharField(max_length=50, blank=True)
    cta_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class BNProcessStep(models.Model):
    about_page = models.ForeignKey(
        BNAboutPage,
        on_delete=models.CASCADE,
        related_name="process_steps"
    )
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

class BNFAQ(models.Model):
    about_page = models.ForeignKey(
        BNAboutPage,
        on_delete=models.CASCADE,
        related_name="faqs"
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question
