from django.core.management.base import BaseCommand

from projects.models import Project
from portfolio_site.utils import extract_video_frame


class Command(BaseCommand):
    help = "Generate a cover thumbnail from the video for projects that have a video but no photo."

    def handle(self, *args, **options):
        qs = Project.objects.exclude(video_file="").filter(thumbnail="", image="")
        if not qs.exists():
            self.stdout.write("No projects need a thumbnail backfill.")
            return

        for project in qs:
            self.stdout.write(f"Extracting frame for: {project.title}")
            frame = extract_video_frame(project.video_file)
            if frame:
                project.thumbnail.save(f"{project.slug}-auto.jpg", frame, save=True)
                self.stdout.write(self.style.SUCCESS(f"  -> saved thumbnail for {project.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"  -> failed to extract frame for {project.title}"))
