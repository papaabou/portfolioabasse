from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import SiteSettings
from projects.models import Skill, Project
from blog.models import Post, Category, Tag
from contact.models import Message
from services.models import Service
from testimonials.models import Testimonial
import random
import datetime


class Command(BaseCommand):
    help = "Seed the database with sample portfolio data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        settings = SiteSettings.load()
        settings.site_title = "Your Name — Web Developer"
        settings.tagline = "Web developer • Shopify expert • Django & JS"
        settings.contact_email = "me@example.com"
        settings.about = (
            "I am a web developer experienced in Python, JavaScript, Django, Flask, and Shopify theme development."
        )
        settings.save()

        skills = [
            ("Python", 90), ("Django", 88), ("JavaScript", 80), ("Node.js", 70), ("Shopify", 95), ("HTML", 85),
        ]
        skill_objs = []
        for name, lvl in skills:
            s, _ = Skill.objects.get_or_create(name=name, defaults={"level": lvl})
            s.level = lvl
            s.save()
            skill_objs.append(s)

        # create sample projects
        sample_projects = [
            {
                "title": "Custom Shopify Theme for Retailer",
                "excerpt": "Built a high-performance, responsive Shopify theme for a retail brand.",
                "description": "Full theme development, liquid templates, custom sections, and app integrations.",
                "url": "",
                "repo_url": "",
                "published": True,
                "featured": True,
            },
            {
                "title": "Django Admin Tool",
                "excerpt": "Internal admin tooling for content management.",
                "description": "A small Django app that improves workflow for editors and content managers.",
                "published": True,
                "featured": False,
            },
        ]

        for p in sample_projects:
            slug = slugify(p["title"])[:220]
            proj, created = Project.objects.get_or_create(slug=slug, defaults={
                "title": p["title"],
                "excerpt": p.get("excerpt", ""),
                "description": p.get("description", ""),
                "url": p.get("url", ""),
                "repo_url": p.get("repo_url", ""),
                "published": p.get("published", True),
                "featured": p.get("featured", False),
            })
            if created:
                proj.technologies.set(random.sample(skill_objs, min(3, len(skill_objs))))
                proj.save()

        # posts
        cat, _ = Category.objects.get_or_create(name="General", slug="general")
        tag, _ = Tag.objects.get_or_create(name="django")
        for i in range(3):
            title = f"Sample Post {i+1}"
            slug = slugify(title)[:240]
            post, _ = Post.objects.get_or_create(slug=slug, defaults={
                "title": title,
                "content": "This is a sample blog post used for seeding the site.",
                "excerpt": "Sample post excerpt",
                "published": True,
            })
            post.categories.add(cat)
            post.tags.add(tag)
            post.save()

        # messages
        for i in range(5):
            Message.objects.get_or_create(
                email=f"user{i}@example.com",
                name=f"User {i}",
                subject=f"Hello {i}",
                body="I would like to work with you. Please contact me.",
                defaults={"is_read": False, "created": datetime.datetime.now()},
            )

        # services
        svc_list = [
            ("Shopify Theme Development", "Custom Shopify themes and Liquid development."),
            ("Django Web Apps", "Full-stack Django applications, APIs and admin tools."),
            ("Integrations & Apps", "Custom apps, webhooks, and third-party integrations."),
        ]
        svc_objs = []
        for idx, (title, desc) in enumerate(svc_list):
            slug = slugify(title)[:220]
            s, _ = Service.objects.get_or_create(slug=slug, defaults={"title": title, "description": desc, "order": idx})
            svc_objs.append(s)

        # testimonials
        for idx in range(3):
            Testimonial.objects.get_or_create(
                name=f"Client {idx+1}",
                company=f"Company {idx+1}",
                body="Great work delivered on time. Highly recommended.",
                defaults={"featured": idx == 0, "order": idx},
            )

        # associate first service with all projects
        for proj in Project.objects.all():
            if svc_objs:
                proj.services.add(svc_objs[0])
                proj.save()

        self.stdout.write(self.style.SUCCESS("Seeding completed."))