import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from client.models import Client
from projects.models import Category, Project, ProjectImage
from services.models import Service

DATA_FILE = Path(__file__).resolve().parent / "data" / "media_library_projects.json"


class Command(BaseCommand):
    help = (
        "Recreate the projects originally imported by seed_media_library.py, "
        "pointing FileFields directly at paths already uploaded to storage "
        "(local media/ or Cloudflare R2), without needing the local source "
        "files (D:\\PORTFOLIO 2026) that command depends on."
    )

    def handle(self, *args, **options):
        with open(DATA_FILE, encoding="utf-8") as f:
            projects_data = json.load(f)

        for data in projects_data:
            category = None
            if data["category"]:
                category = Category.objects.filter(name=data["category"]).first()
                if category is None:
                    category, _ = Category.objects.get_or_create(
                        slug=slugify(data["category"]),
                        defaults={"name": data["category"]},
                    )

            client = None
            if data["client"]:
                client, _ = Client.objects.get_or_create(name=data["client"])

            project, _ = Project.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "category": category,
                    "client": client,
                    "excerpt": data["excerpt"],
                    "description": data["description"],
                    "year": data["year"],
                    "featured": data["featured"],
                    "published": data["published"],
                    "video_url": data["video_url"] or "",
                },
            )

            if data["thumbnail"]:
                project.thumbnail.name = data["thumbnail"]
            if data["image"]:
                project.image.name = data["image"]
            if data["video_file"]:
                project.video_file.name = data["video_file"]
            project.save()

            services = Service.objects.filter(slug__in=data["services"])
            project.services.set(services)

            existing_gallery = list(project.images.all())
            for i, item in enumerate(data["gallery"]):
                if i < len(existing_gallery):
                    gi = existing_gallery[i]
                else:
                    gi = ProjectImage(project=project)
                gi.image.name = item["image"]
                gi.caption = item["caption"]
                gi.order = item["order"]
                gi.save()

        self.stdout.write(self.style.SUCCESS(
            f"Recreated {len(projects_data)} projects from {DATA_FILE.name}."
        ))
