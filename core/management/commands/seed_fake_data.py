from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
try:
    from faker import Faker
except Exception:
    Faker = None
import random

from projects.models import Skill, Client, Project, ProjectSection
from services.models import Service
from testimonials.models import Testimonial
from contact.models import Message
from blog.models import Post, Category, Tag
from core.models import SiteSettings


class Command(BaseCommand):
    help = "Wipe project data and seed realistic fake data (preserves Osama Abdullah user info)."

    def handle(self, *args, **options):
        if Faker:
            fake = Faker()
        else:
            # minimal fallback generator
            class _Fallback:
                def name(self):
                    first = random.choice(["John","Jane","Alex","Sam","Taylor","Jordan","Chris","Morgan"]) 
                    last = random.choice(["Smith","Doe","Brown","Lee","Garcia","Patel","Khan","Wright"]) 
                    return f"{first} {last}"

                def company(self):
                    return random.choice(["Acme Co","Globex","Initech","Umbrella","Stark Industries","Wayne Enterprises"]) 

                def company_email(self):
                    return f"contact@{random.choice(["example.com","acme.com","globex.com"])}"

                def phone_number(self):
                    return f"+1{random.randint(2000000000,9999999999)}"

                def url(self):
                    return f"https://{random.choice(["example.com","acme.com","globex.com"])}"

                def catch_phrase(self):
                    return random.choice(["Next-gen e-commerce","Holistic storefronts","Scalable commerce solutions"]) 

                def paragraph(self, nb_sentences=3):
                    return " ".join(["Lorem ipsum dolor sit amet." for _ in range(nb_sentences)])

                def sentence(self, nb_words=6):
                    return "Lorem ipsum dolor sit amet."

                def email(self):
                    return f"user{random.randint(1,999)}@example.com"

                def sentence(self, nb_words=20):
                    return "Lorem ipsum dolor sit amet."

                def uri_path(self):
                    return "/repo/url"

            fake = _Fallback()

        self.stdout.write("Clearing selected models...")

        # Delete dependent/child models first
        ProjectSection.objects.all().delete()
        Testimonial.objects.all().delete()
        Project.objects.all().delete()
        Client.objects.all().delete()
        Skill.objects.all().delete()
        Service.objects.all().delete()
        Message.objects.all().delete()
        Post.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()

        # Reset site settings
        SiteSettings.objects.all().delete()

        # Remove all users (we'll recreate Osama below)
        User = get_user_model()
        User.objects.all().delete()

        # Create Osama Abdullah user (preserved identity)
        self.stdout.write("Creating user Osama Abdullah...")
        osama = User.objects.create_user(
            username="osama",
            email="osama@example.com",
            password="password",
            first_name="Osama",
            last_name="Abdullah",
        )
        try:
            osama.is_staff = True
            osama.is_superuser = True
            osama.save()
        except Exception:
            # some custom user models may not have these fields
            pass

        # Create site settings with preserved name/profession
        ss = SiteSettings(
            site_title=f"Osama Abdullah — Shopify Developer",
            tagline="Shopify themes, apps & store builds",
            about=(
                "Osama Abdullah is a Shopify Developer specializing in theme development, app integration, "
                "and store migrations. This site is populated with fake data for testing purposes."
            ),
            contact_email="osama@example.com",
            github=f"https://github.com/osama",
            twitter=f"https://twitter.com/osama",
            linkedin=f"https://linkedin.com/in/osama",
        )
        ss.save()

        # Skills
        skills_list = [
            "Shopify",
            "Liquid",
            "HTML",
            "CSS",
            "JavaScript",
            "Python",
            "Django",
            "GraphQL",
            "REST APIs",
            "Git",
            "SEO",
            "Performance Optimization",
        ]

        skills = []
        for name in skills_list:
            s = Skill.objects.create(name=name, level=random.randint(50, 100), order=random.randint(0, 20))
            skills.append(s)

        # Services
        service_titles = [
            "Shopify Theme Development",
            "Shopify Store Setup",
            "App Integration",
            "Performance Optimization",
            "Migrate to Shopify",
        ]
        services = []
        for idx, title in enumerate(service_titles):
            svc = Service.objects.create(title=title, slug=slugify(title)[:220], description=fake.paragraph(), order=idx)
            services.append(svc)

        # Clients
        clients = []
        for _ in range(8):
            name = fake.name()
            company = fake.company()
            c = Client.objects.create(
                name=name,
                company_name=company,
                email=fake.company_email(),
                whatsapp=fake.phone_number(),
                website=fake.url(),
            )
            clients.append(c)

        # Projects
        projects = []
        for i in range(12):
            title = f"{fake.catch_phrase()}"
            slug = slugify(title)[:220]
            client = random.choice(clients + [None])
            proj = Project.objects.create(
                title=title,
                slug=slug,
                client=client,
                excerpt=fake.sentence(nb_words=20),
                hero_description=fake.paragraph(nb_sentences=3),
                live_url=fake.url(),
                repo_url=fake.uri_path(),
                featured=(i % 6 == 0),
                published=True,
                timeline=fake.sentence(nb_words=4),
                year=random.randint(2018, 2025),
            )
            # add m2m technologies and services
            proj.technologies.set(random.sample(skills, k=random.randint(1, min(5, len(skills)))))
            proj.services.set(random.sample(services, k=random.randint(1, min(3, len(services)))))
            projects.append(proj)

            # add a couple of sections
            for j in range(2):
                ProjectSection.objects.create(
                    project=proj,
                    heading=fake.sentence(nb_words=6),
                    subheading=fake.sentence(nb_words=8),
                    body=fake.paragraph(nb_sentences=4),
                    order=j,
                    is_highlight=(j == 0 and random.choice([True, False]))
                )

        # Testimonials
        for _ in range(8):
            client = random.choice(clients)
            project = random.choice(projects)
            Testimonial.objects.create(
                client=client,
                project=project,
                name=fake.name(),
                role=fake.job(),
                company=client.company_name or fake.company(),
                body=fake.paragraph(nb_sentences=3),
                email=fake.email(),
                featured=random.choice([False, True]),
                approved=True,
            )

        # Blog: categories, tags, posts
        cat_objs = []
        for title in ["Announcements", "Tutorials", "Case Studies", "News"]:
            c = Category.objects.create(name=title, slug=slugify(title)[:140])
            cat_objs.append(c)

        tag_objs = []
        for t in ["shopify", "theme", "performance", "seo", "development"]:
            tg = Tag.objects.create(name=t)
            tag_objs.append(tg)

        for _ in range(6):
            title = fake.sentence(nb_words=6)
            post = Post.objects.create(
                title=title,
                slug=slugify(title)[:240],
                author=osama,
                content=fake.paragraph(nb_sentences=8),
                excerpt=fake.sentence(nb_words=20),
                published=True,
            )
            post.categories.set(random.sample(cat_objs, k=random.randint(1, len(cat_objs))))
            post.tags.set(random.sample(tag_objs, k=random.randint(1, len(tag_objs))))

        # Contact messages
        for _ in range(10):
            Message.objects.create(
                name=fake.name(),
                email=fake.email(),
                service=random.choice(services + [None]),
                budget=round(random.uniform(100.0, 20000.0), 2),
                body=fake.paragraph(nb_sentences=3),
                is_read=random.choice([False, True]),
            )

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
        # Summary counts
        counts = {
            "users": User.objects.count(),
            "skills": Skill.objects.count(),
            "services": Service.objects.count(),
            "clients": Client.objects.count(),
            "projects": Project.objects.count(),
            "sections": ProjectSection.objects.count(),
            "testimonials": Testimonial.objects.count(),
            "posts": Post.objects.count(),
            "categories": Category.objects.count(),
            "tags": Tag.objects.count(),
            "messages": Message.objects.count(),
        }
        for k, v in counts.items():
            self.stdout.write(f"{k}: {v}")
