from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

try:
    # Django 3.1+ builtin JSONField
    from django.db.models import JSONField
except Exception:
    # Fallback for older Django (if using django-jsonfield or similar)
    JSONField = None

class SiteSettings(models.Model):
    # Site Info
    site_title = models.CharField(max_length=200, default="My Portfolio")
    tagline = models.CharField(max_length=250, blank=True)
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        help_text="Upload favicon (16x16 or 32x32, max 100KB)"
    )

    def clean(self):
        super().clean()
        if self.favicon and self.favicon.size > 102400:
            raise ValidationError({
                "favicon": "Favicon file size must be under 100KB."
            })

    # Footer / About
    about_short = models.TextField(blank=True)
    footer_text = models.TextField(blank=True)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to="site/seo/", blank=True, null=True)
    twitter_card = models.CharField(max_length=50, default="summary_large_image", blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SeoMixin(models.Model):
    """
    Abstract mixin to add basic SEO / OpenGraph fields to content models.
    """
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    canonical_url = models.URLField(blank=True, null=True)

    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to="seo/og/", blank=True, null=True)

    robots = models.CharField(
        max_length=50, blank=True, default="index,follow",
        help_text="Comma-separated robots directives, e.g. 'noindex,nofollow'"
    )

    class Meta:
        abstract = True


class ContentBlock(models.Model):
    """
    Generic, orderable content blocks attachable to any model instance.
    Useful for building flexible CMS-like page sections.
    """
    TEXT = "text"
    IMAGE = "image"
    HTML = "html"

    BLOCK_TYPE_CHOICES = [
        (TEXT, "Text"),
        (IMAGE, "Image"),
        (HTML, "HTML"),
    ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    block_type = models.CharField(max_length=20, choices=BLOCK_TYPE_CHOICES, default=TEXT)
    heading = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="content_blocks/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    extra = JSONField(blank=True, null=True) if JSONField is not None else None

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.content_type} — {self.heading or self.block_type}"


class FAQItem(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Question fréquente"
        verbose_name_plural = "Questions fréquentes (FAQ)"

    def __str__(self):
        return self.question
