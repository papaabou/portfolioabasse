from django.db import models
from datetime import date
from projects.models import Skill
from core.models import SeoMixin

class Profile(models.Model):
    full_name = models.CharField(max_length=100)
    short_bio = models.TextField(
        help_text="Short paragraph for homepage bento box",
        blank=True,
    )

    philosophy = models.TextField(
        help_text="Write about your Philosophy",
        blank=True,
    )

    profile_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )

    # Contact fields
    email = models.EmailField(blank=True, help_text="Primary contact email for the site owner")
    whatsapp = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="profiles"
    )

    is_active = models.BooleanField(default=True)

    career_start_date = models.DateField(
        help_text="When your professional journey started",
        blank=True,
        null=True,
    )

    def years_of_experience(self):
        if not self.career_start_date:
            return 0
        today = date.today()
        years = today.year - self.career_start_date.year

        # adjust if anniversary not reached yet
        if (today.month, today.day) < (
            self.career_start_date.month,
            self.career_start_date.day,
        ):
            years -= 1

        return max(years, 0)

    def save(self, *args, **kwargs):
        """Enforce a single instance by always using PK=1."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"full_name": "Your Name"})
        return obj

    def __str__(self):
        return self.full_name

class Journey(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="journeys"
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    start_year = models.CharField(max_length=20)
    end_year = models.CharField(max_length=20, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class CoreValue(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="values"
    )
    title = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class SocialLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="social_links")
    platform_name = models.CharField(max_length=50, help_text="e.g., GitHub, LinkedIn")
    url = models.URLField(help_text="Full URL to your social profile")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.platform_name} ({self.url})"

class AboutSettings(SeoMixin, models.Model):
    hero_title = models.CharField(
        max_length=255,
        default="The Architect Behind the Code"
    )
    hero_subtitle = models.TextField(
        default="I believe that true digital craftsmanship requires more than just technical skill—it requires empathy, vision, and a deep appreciation for detail."
    )
    hero_image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "About Page Settings"
        verbose_name_plural = "About Page Settings"

    def __str__(self):
        return "About Page Settings"

    def save(self, *args, **kwargs):
        """
        Ensure only one instance exists.
        """
        self.pk = 1
        super().save(*args, **kwargs)
