from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from projects.models import Category, Project
from services.models import Service
from about_me.models import Profile
from .models import FAQItem


SHOWREEL_SLUGS = ["showreel-creation-digitale", "showreel-audiovisuel-montage"]


def home(request):
    profile = Profile.load()
    published = Project.objects.filter(published=True)
    projects = published.exclude(slug__in=SHOWREEL_SLUGS).select_related("category", "client").prefetch_related("services")[:6]
    project_count = published.count()
    categories = Category.objects.all()[:6]
    services = Service.objects.filter(published=True).order_by("order", "title")[:6]
    showreels = list(published.filter(slug__in=SHOWREEL_SLUGS))
    return render(request, "core/home.html", {
        "projects": projects,
        "project_count": project_count,
        "categories": categories,
        "services": services,
        "profile": profile,
        "showreels": showreels,
    })


def faq_view(request):
    faqs = FAQItem.objects.filter(published=True)
    return render(request, "core/faq.html", {"faqs": faqs})


def mentions_legales_view(request):
    profile = Profile.load()
    return render(request, "core/mentions_legales.html", {"profile": profile})


def politique_confidentialite_view(request):
    profile = Profile.load()
    return render(request, "core/politique_confidentialite.html", {"profile": profile})


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Allow: /",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
