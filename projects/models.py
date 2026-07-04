from django.db import models

from client.models import Client
from core.models import SeoMixin
from services.models import Service


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(default=1, help_text="1-100")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-level", "order"]

    def __str__(self):
        return self.name


class Project(SeoMixin, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    excerpt = models.TextField(blank=True)
    hero_description = models.TextField(blank=True)
    description = models.TextField(blank=True, help_text="Description detaillee du projet")
    year = models.PositiveSmallIntegerField(blank=True, null=True)

    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True, help_text="Lien YouTube ou Vimeo")
    video_file = models.FileField(upload_to="projects/videos/", blank=True, null=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="projects/thumbnails/",
        blank=True,
        null=True,
        help_text="Image principale du projet",
    )

    services = models.ManyToManyField(Service, blank=True, related_name="projects")
    technologies = models.ManyToManyField(Skill, blank=True, related_name="projects")

    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    timeline = models.CharField(max_length=100, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-featured", "-created"]

    def __str__(self):
        return self.title

    @property
    def cover_image(self):
        return self.thumbnail or self.image

    @property
    def video_embed_url(self):
        if not self.video_url:
            return ""

        url = self.video_url.strip()
        if "youtube.com/watch?v=" in url:
            return url.replace("watch?v=", "embed/")
        if "youtu.be/" in url:
            video_id = url.rstrip("/").split("/")[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        if "vimeo.com/" in url and "player.vimeo.com" not in url:
            video_id = url.rstrip("/").split("/")[-1]
            return f"https://player.vimeo.com/video/{video_id}"
        return url


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/images/")
    caption = models.CharField(max_length=220, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} image ({self.id})"


class ProjectSection(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sections")
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=300, blank=True)
    body = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    is_highlight = models.BooleanField(
        default=False,
        help_text="Use for testimonials, results, or special callouts",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.heading
