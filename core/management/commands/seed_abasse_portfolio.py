import io

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image

from django.contrib.sites.models import Site

from about_me.models import Profile, SocialLink
from blog.models import Post
from client.models import Client
from contact.models import ContactSettings
from core.models import FAQItem, SiteSettings
from projects.models import Category, Project
from services.models import Service
from testimonials.models import TestimonialPageSettings


TAGLINE = (
    "Abasse NIANG — Graphiste & Créateur Visuel basé à Créteil.\n"
    "Je crée des visuels, vidéos, miniatures, chartes graphiques et contenus digitaux "
    "pour marques, créateurs et entreprises."
)

# Slugs of older placeholder projects replaced by real, sourced work.
OBSOLETE_PROJECT_SLUGS = [
    "videos-interviews-feed-back",
    "montage-video-championnat-de-france-des-sc",
    "portfolio",
    "refonte-du-site-kraft-heinz",
    "charte-graphique-balde-afro-gourmet",
]


class Command(BaseCommand):
    help = "Prepare the portfolio content for Abasse NIANG."

    def handle(self, *args, **options):
        settings = SiteSettings.load()
        settings.site_title = "Abasse NIANG"
        settings.tagline = "Graphiste & Créateur Visuel basé à Créteil"
        settings.about_short = TAGLINE
        settings.footer_text = "Graphiste, créateur visuel et monteur vidéo basé à Créteil."
        settings.meta_title = "Abasse NIANG | Graphiste & Créateur Visuel"
        settings.meta_description = "Portfolio d'Abasse NIANG, graphiste, créateur visuel et monteur vidéo à Créteil."
        settings.save()

        profile = Profile.load()
        profile.full_name = "Abasse NIANG"
        profile.short_bio = (
            "Graphiste, monteur vidéo et motion designer basé à Créteil. J'habille des chaînes "
            "de télévision, je monte des émissions et je construis des identités visuelles pour "
            "des marques et des créateurs."
        )
        profile.philosophy = (
            "Mon travail est né dans la vidéo : clips musicaux, habillages de chaînes comme "
            "IDF TV, Val-d'Oise TV ou D5 Media, génériques d'émissions comme Top Clips. Cette "
            "exigence de rythme et de lisibilité, je l'applique à tout ce que je crée — "
            "miniatures, chartes graphiques, visuels de marque. Un bon visuel se comprend en "
            "une seconde et donne envie de rester."
        )
        profile.is_active = True
        profile.save()

        SocialLink.objects.update_or_create(
            profile=profile,
            platform_name="Behance",
            defaults={"url": "https://www.behance.net/abasseniang1", "order": 1},
        )
        SocialLink.objects.update_or_create(
            profile=profile,
            platform_name="LinkedIn",
            defaults={"url": "https://www.linkedin.com/in/abasse-niang-93a835260/", "order": 2},
        )
        SocialLink.objects.update_or_create(
            profile=profile,
            platform_name="Instagram",
            defaults={"url": "https://www.instagram.com/bassit_prod/", "order": 3},
        )
        SocialLink.objects.update_or_create(
            profile=profile,
            platform_name="TikTok",
            defaults={"url": "https://www.tiktok.com/@bassit_prod98", "order": 4},
        )

        ContactSettings.objects.update_or_create(
            pk=1,
            defaults={
                "sender_name": "Abasse NIANG",
                "recipient_email": "papeaboumbaye@gmail.com",
            },
        )
        TestimonialPageSettings.objects.get_or_create(pk=1)

        # Placeholder production domain used for the sitemap until the real
        # domain name is purchased/confirmed — update via Django admin (Sites).
        Site.objects.update_or_create(
            pk=1,
            defaults={"domain": "abasseniang.fr", "name": "Abasse NIANG"},
        )

        # Rename the old "Photo e-commerce" / "Photo" category row in place
        # (see the matching Service rename below) rather than leaving an
        # orphaned row behind.
        Category.objects.filter(slug__in=["photo-e-commerce", "photo"]).update(slug="photos", name="Photos")

        categories = {
            "design": self.category("Design graphique"),
            "video": self.category("Montage vidéo"),
            "thumbnail": self.category("Miniatures"),
            "branding": self.category("Charte graphique"),
            "web": self.category("Web design"),
            "photo": self.category("Photos"),
        }

        # "Photo e-commerce" was renamed to "Photo" then to "Photos" — no
        # e-commerce product shots existed at first, so the narrower promise
        # didn't match the portfolio. Rename the old row in place rather than
        # leaving an orphaned service behind.
        Service.objects.filter(slug__in=["photo-e-commerce", "photo"]).update(slug="photos")

        services = {
            "visuels": self.service("Création visuelle", "Visuels digitaux, bannières, compositions et contenus de marque.", 1, icon="bi-palette2"),
            "video": self.service("Montage vidéo", "Montage d'interviews, chaînes YouTube, formats courts et contenus sociaux.", 2, icon="bi-film"),
            "thumbnail": self.service("Miniatures YouTube", "Miniatures lisibles, contrastées et pensées pour le clic.", 3, icon="bi-image"),
            "branding": self.service("Charte graphique", "Logo, couleurs, typographies et univers visuel.", 4, icon="bi-vector-pen"),
            "web": self.service("Web design", "Refontes graphiques et maquettes de sites.", 5, icon="bi-window"),
            "photo": self.service("Photos", "Retouche et mise en valeur de photos produits et portraits.", 6, icon="bi-camera"),
        }

        fast_genius = self.client("Fast & Genius")

        Project.objects.filter(slug__in=OBSOLETE_PROJECT_SLUGS).delete()

        # Rename the old "Photos E-commerce" / "Photo" placeholder in place.
        Project.objects.filter(slug__in=["photos-e-commerce", "photo"]).update(slug="photos")

        projects = [
            {
                "title": "Bannière TV",
                "category": categories["design"],
                "services": ["visuels"],
                "description": "Création d'une bannière TV claire, impactante et prête pour diffusion.",
                "featured": True,
            },
            # The following entries have no real image or video to back them —
            # kept in the seed for historical/reference purposes, but explicitly
            # unpublished so they never show up as empty placeholders on the
            # live site. Add a real image via the dashboard and flip
            # "published" to True (or just publish it from Django admin) once
            # real visuals exist.
            {
                "title": "Montage vidéo Chaîne YouTube BAADOOLA TV",
                "category": categories["video"],
                "services": ["video"],
                "description": "Montage vidéo pour chaîne YouTube avec habillage et rythme éditorial.",
                "featured": True,
                "published": False,
            },
            {
                "title": "Miniatures Mini Formation REBOOT",
                "category": categories["thumbnail"],
                "services": ["thumbnail"],
                "description": "Série de miniatures pour formation, pensées pour attirer l'attention rapidement.",
                "featured": True,
                "published": False,
            },
            {
                "title": "Miniaturs",
                "category": categories["thumbnail"],
                "services": ["thumbnail"],
                "description": "Création de miniatures digitales au style direct, lisible et contrasté.",
                "featured": False,
                "published": False,
            },
            {
                "title": "Photos",
                "category": categories["photo"],
                "services": ["photo"],
                "description": "Séance photo produit pour la boutique e-commerce de mode Lachica (lachica.fr) : "
                                "mises en scène en extérieur et en intérieur pour présenter les vêtements et "
                                "accessoires de la collection dans un style lifestyle.",
                "featured": False,
            },
            # Interviews montées pour la chaîne Fast & Genius / Championnat de France des Sports du Cerveau
            {
                "title": "Rafael MOYA, notre commissaire de justice",
                "category": categories["video"],
                "services": ["video", "thumbnail"],
                "description": "Montage d'une interview pour la chaîne Fast & Genius, mettant en lumière le métier de commissaire de justice à travers le témoignage de Rafael Moya.",
                "featured": False,
                "client": fast_genius,
                "video_url": "https://youtu.be/Kne4qArnTIU",
            },
            {
                "title": "KAMEL KAJOUT - Êtes-vous prêt à hacker votre mémoire ?",
                "category": categories["video"],
                "services": ["video"],
                "description": "Montage d'une interview pour Fast & Genius sur les techniques de mémorisation, avec Kamel Kajout.",
                "featured": False,
                "client": fast_genius,
                "video_url": "https://youtu.be/SuO7b5ePPgE",
            },
            {
                "title": "L'influence cachée du cerveau humain - Guillaume Attias",
                "category": categories["video"],
                "services": ["video"],
                "description": "Montage vidéo pour le Championnat de France des Sports du Cerveau : interview de Guillaume Attias sur l'influence du cerveau humain, réalisée pour Fast & Genius.",
                "featured": True,
                "client": fast_genius,
                "video_url": "https://youtu.be/3PsKFBrFtT8",
            },
            {
                "title": "Comment nourrir votre cerveau ? - Mohamed Chayani",
                "category": categories["video"],
                "services": ["video"],
                "description": "Interview montée pour le Championnat de France des Sports du Cerveau, avec Mohamed Chayani sur l'alimentation du cerveau.",
                "featured": False,
                "client": fast_genius,
                "video_url": "https://youtu.be/sQf4_nxM9Ks",
            },
            {
                "title": "La maladie est une chance - Paul Fontaine",
                "category": categories["video"],
                "services": ["video"],
                "description": "Montage d'un témoignage fort pour le Championnat de France des Sports du Cerveau, avec Paul Fontaine, pour la chaîne Fast & Genius.",
                "featured": False,
                "client": fast_genius,
                "video_url": "https://youtu.be/DMCglIXqgc4",
            },
            {
                "title": "Jottay Bi",
                "category": categories["video"],
                "services": ["video"],
                "description": "Montage vidéo réalisé pour la chaîne YouTube personnelle Bassit Prod, avec habillage et rythme propres à l'univers de la chaîne.",
                "featured": False,
                "video_url": "https://youtu.be/T5D-xMzvoKA",
            },
        ]

        for data in projects:
            slug = slugify(data["title"])
            project, _ = Project.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": data["title"],
                    "category": data["category"],
                    "client": data.get("client"),
                    "excerpt": data["description"],
                    "description": data["description"],
                    "year": 2026,
                    "featured": data["featured"],
                    "published": data.get("published", True),
                    "video_url": data.get("video_url", ""),
                },
            )
            project.services.set([services[key] for key in data["services"]])

            video_url = data.get("video_url")
            if video_url and not project.thumbnail:
                self.attach_youtube_thumbnail(project, video_url)

        self.seed_blog_posts()
        self.seed_faq()

        self.stdout.write(self.style.SUCCESS("Portfolio Abasse NIANG prepare avec succes."))

    def seed_blog_posts(self):
        posts = [
            {
                "title": "Comment choisir la bonne miniature YouTube pour booster son taux de clic",
                "excerpt": "Une miniature efficace se décide en une fraction de seconde. Voici les principes qui font la différence entre une miniature ignorée et une miniature qui capte le clic.",
                "content": (
                    "Sur YouTube, la miniature est souvent plus déterminante que le titre : c'est le "
                    "premier élément visuel que l'œil capte dans un flux de recommandations saturé. "
                    "Voici les principes qui reviennent sur les miniatures qui fonctionnent.\n\n"
                    "**1. Un point focal unique.** Une miniature efficace raconte une seule idée, pas "
                    "trois. Trop d'éléments (texte, visage, flèches, logos) diluent l'attention et "
                    "rendent l'image illisible en petit format, notamment sur mobile.\n\n"
                    "**2. Un contraste fort.** Les miniatures qui se détachent dans un flux utilisent "
                    "des couleurs contrastées entre le sujet et l'arrière-plan, pas nécessairement des "
                    "couleurs vives à tout prix, mais un écart de luminosité net.\n\n"
                    "**3. Une expression ou un objet qui intrigue.** Un visage exprimant une émotion "
                    "claire (surprise, doute, joie) ou un objet inattendu donne une raison de cliquer "
                    "pour comprendre le contexte.\n\n"
                    "**4. Un texte minimal, s'il y en a un.** 2 à 4 mots maximum, en gras, lisibles même "
                    "en miniature 120x90px. Le texte doit compléter le titre, jamais le répéter.\n\n"
                    "**5. Une cohérence avec le contenu réel.** Le clic-bait qui ne tient pas sa promesse "
                    "abîme la rétention et le rythme de visionnage, ce qui pénalise la vidéo sur le long "
                    "terme. Une bonne miniature est honnête autant qu'efficace.\n\n"
                    "En pratique, je teste toujours plusieurs versions avant de livrer une miniature "
                    "finale, en réduisant l'aperçu à la taille réelle d'affichage pour vérifier sa "
                    "lisibilité avant validation."
                ),
            },
            {
                "title": "Charte graphique : pourquoi c'est l'investissement le plus rentable pour une marque",
                "excerpt": "Logo, couleurs, typographies : une charte graphique claire évite l'improvisation visuelle et fait gagner du temps sur chaque support futur.",
                "content": (
                    "Beaucoup de marques et de créateurs repoussent la charte graphique, la considérant "
                    "comme un luxe réservé aux grandes entreprises. En réalité, c'est souvent l'inverse : "
                    "plus une structure est petite, plus une charte claire lui fait gagner du temps.\n\n"
                    "**Ce que couvre une charte graphique.** Logo (et ses déclinaisons), palette de "
                    "couleurs précise, typographies principales et secondaires, règles d'usage (espacements, "
                    "tailles minimales, ce qu'il ne faut pas faire), et parfois un ton visuel général "
                    "(photographie, iconographie, style d'illustration).\n\n"
                    "**Pourquoi ça change tout au quotidien.** Sans charte, chaque nouveau support "
                    "(post réseau social, bannière, présentation, miniature) repart de zéro : nouvelles "
                    "couleurs choisies à l'instinct, nouvelle typographie, incohérences qui s'accumulent. "
                    "Avec une charte, ces décisions sont déjà prises une fois pour toutes, et le rendu "
                    "reste reconnaissable sur tous les supports.\n\n"
                    "**Un accélérateur pour l'équipe ou les prestataires.** Une charte bien documentée "
                    "permet à n'importe quel graphiste ou monteur vidéo de produire un contenu cohérent "
                    "avec la marque, sans allers-retours interminables de validation.\n\n"
                    "**Le bon moment pour investir.** Dès qu'une marque publie régulièrement du contenu "
                    "ou qu'elle prévoit de déléguer une partie de sa création visuelle, la charte "
                    "graphique devient rentable presque immédiatement : elle évite de refaire le travail "
                    "et accélère chaque nouvelle production."
                ),
            },
            {
                "title": "5 conseils pour un montage vidéo qui capte l'attention dès les 3 premières secondes",
                "excerpt": "Sur les plateformes actuelles, l'attention se joue en quelques secondes. Voici les leviers de montage qui font la différence dès le début d'une vidéo.",
                "content": (
                    "Sur YouTube comme sur les formats courts, la majorité du décrochage se joue dans "
                    "les premières secondes. Voici les leviers de montage qui aident à garder l'audience "
                    "au-delà de ce point critique.\n\n"
                    "**1. Ne pas commencer par une introduction longue.** Logo animé de 5 secondes, "
                    "générique, mise en contexte trop détaillée : autant d'éléments à repousser après "
                    "avoir capté l'attention, pas avant.\n\n"
                    "**2. Ouvrir sur la promesse ou le moment fort.** Montrer immédiatement ce que la "
                    "vidéo va apporter, ou un extrait marquant qui sera développé plus loin, donne une "
                    "raison concrète de rester.\n\n"
                    "**3. Rythmer avec des coupes franches.** Éliminer les silences, hésitations et "
                    "temps morts au montage resserre le rythme sans dénaturer le propos.\n\n"
                    "**4. Habiller visuellement sans surcharger.** Sous-titres, incrustations et "
                    "transitions doivent servir la lisibilité et le rythme, pas distraire du contenu "
                    "principal.\n\n"
                    "**5. Soigner le son autant que l'image.** Un mixage propre, sans niveaux sonores "
                    "irréguliers, retient davantage qu'une image léchée avec un son négligé — l'oreille "
                    "pardonne moins que l'œil.\n\n"
                    "Ces principes s'appliquent aussi bien à une interview, un montage sportif qu'à un "
                    "format court pour réseaux sociaux : seul le rythme d'application change."
                ),
            },
        ]

        for index, data in enumerate(posts, start=1):
            Post.objects.update_or_create(
                slug=slugify(data["title"]),
                defaults={
                    "title": data["title"],
                    "excerpt": data["excerpt"],
                    "content": data["content"].replace("**", ""),
                    "published": True,
                },
            )

    def seed_faq(self):
        faqs = [
            (
                "Quels types de projets peux-tu réaliser ?",
                "Montage vidéo (interviews, formats YouTube, contenus courts), miniatures YouTube, "
                "charte graphique et identité visuelle, web design et refonte graphique, ainsi que "
                "la retouche de photos e-commerce.",
            ),
            (
                "Quel est le délai moyen pour un projet ?",
                "Cela dépend du type de projet : une miniature ou un visuel simple peut être livré en "
                "quelques jours, un montage vidéo complet ou une charte graphique complète prend "
                "généralement 1 à 3 semaines. Le délai exact est toujours précisé dans le devis.",
            ),
            (
                "Comment se déroule une collaboration ?",
                "Tout commence par un échange sur votre projet (via le formulaire de devis ou de "
                "contact), suivi d'une proposition avec délai et tarif. Une fois validée, je travaille "
                "par étapes avec des points de validation réguliers jusqu'à la livraison finale.",
            ),
            (
                "Combien de révisions sont incluses ?",
                "Le nombre de révisions dépend du type de prestation et est précisé dans chaque devis. "
                "L'objectif est toujours d'arriver à un résultat qui vous convient pleinement.",
            ),
            (
                "Travailles-tu avec des particuliers et des entreprises ?",
                "Les deux : créateurs de contenu, indépendants, petites entreprises et marques plus "
                "établies. Chaque projet est adapté au besoin et au budget réels du client.",
            ),
            (
                "Comment obtenir un devis ?",
                "Le plus simple est de remplir le formulaire de demande de devis avec quelques détails "
                "sur votre projet : je reviens vers vous sous 24 à 48h avec une proposition adaptée, "
                "sans engagement.",
            ),
        ]

        for index, (question, answer) in enumerate(faqs, start=1):
            FAQItem.objects.update_or_create(
                question=question,
                defaults={"answer": answer, "order": index, "published": True},
            )

    def category(self, name):
        return Category.objects.update_or_create(
            slug=slugify(name),
            defaults={"name": name},
        )[0]

    def service(self, title, description, order, icon=""):
        return Service.objects.update_or_create(
            slug=slugify(title),
            defaults={
                "title": title,
                "description": description,
                "order": order,
                "published": True,
                "icon": icon,
            },
        )[0]

    def client(self, name):
        return Client.objects.update_or_create(name=name, defaults={})[0]

    def attach_youtube_thumbnail(self, project, video_url):
        video_id = video_url.rstrip("/").split("/")[-1].split("?")[0]
        if not video_id:
            return

        for quality in ("maxresdefault", "hqdefault"):
            image_url = f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"
            try:
                response = requests.get(image_url, timeout=10)
            except requests.RequestException:
                continue

            if response.status_code == 200 and len(response.content) > 2000:
                compressed = self.compress_image(response.content)
                project.thumbnail.save(
                    f"{project.slug}.jpg",
                    ContentFile(compressed),
                    save=True,
                )
                return

    def compress_image(self, raw_bytes, max_width=1280, quality=82):
        """Resize to a sane max width and re-encode as JPEG to keep media light."""
        try:
            image = Image.open(io.BytesIO(raw_bytes))
            image = image.convert("RGB")
            if image.width > max_width:
                ratio = max_width / float(image.width)
                image = image.resize((max_width, int(image.height * ratio)), Image.LANCZOS)
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=quality, optimize=True)
            return buffer.getvalue()
        except Exception:
            return raw_bytes
