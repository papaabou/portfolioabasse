from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post
from projects.models import Project
from services.models import Service


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return [
            "home",
            "service_list",
            "realisations",
            "gallery",
            "about",
            "post_list",
            "testimonials_list",
            "faq",
            "contact",
            "devis",
            "mentions_legales",
            "politique_confidentialite",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "home" else 0.6


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse("realisation_detail", args=[obj.slug])


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Service.objects.filter(published=True)

    def location(self, obj):
        return reverse("service_detail", args=[obj.slug])


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse("post_detail", args=[obj.slug])
