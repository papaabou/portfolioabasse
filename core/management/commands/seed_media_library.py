import io
from pathlib import Path

import cv2
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image

from client.models import Client
from projects.models import Category, Project, ProjectImage
from services.models import Service

SOURCE_DIR = Path(r"D:\PORTFOLIO 2026")

# Videos above this size are not copied as playable files (kept as thumbnail-only
# entries) to avoid bloating media storage with an unoptimized export.
MAX_VIDEO_BYTES = 150 * 1024 * 1024


def find_file(folder, contains):
    """Locate a file under SOURCE_DIR/folder whose name contains an ASCII-safe
    substring, sidestepping fragile accented-filename transcription."""
    base = SOURCE_DIR / folder if folder else SOURCE_DIR
    if not base.exists():
        return None
    contains_lower = contains.lower()
    for path in base.iterdir():
        if path.is_file() and contains_lower in path.name.lower():
            return path
    return None


class Command(BaseCommand):
    help = "Import real media assets (videos, banners) from the local portfolio archive."

    def handle(self, *args, **options):
        if not SOURCE_DIR.exists():
            self.stdout.write(self.style.ERROR(f"Source folder introuvable : {SOURCE_DIR}"))
            return

        category = self.category("Motion Design & Habillage TV")
        service = self.service("Habillage TV & Motion Design",
                                "Habillages de chaîne, jingles animés, intros d'émissions et identités de marque en mouvement.",
                                order=7)
        video_service = Service.objects.filter(slug="montage-video").first()
        design_service = Service.objects.filter(slug="creation-visuelle").first()
        branding_service = Service.objects.filter(slug="charte-graphique").first()

        d5 = self.client("D5 Media")
        idf_tv = self.client("IDF TV")
        val_doise_tv = self.client("Val-d'Oise TV")
        top_clips = self.client("Top Clips")

        # ------------------------------------------------------------------
        # 1. D5 Media — identité de marque (4 bannières + logo animé)
        # ------------------------------------------------------------------
        d5_project = self.upsert_project(
            title="Identité visuelle D5 Media — Radio, TV, Music, News",
            category=self.category("Charte graphique"),
            client=d5,
            services=[s for s in [branding_service, service] if s],
            excerpt="Bannières harmonisées et logo animé pour les quatre antennes du groupe D5.",
            description=(
                "D5 Media regroupe quatre antennes distinctes — Radio, TV, Music et News — qui "
                "avaient besoin d'une signature visuelle commune sans perdre l'identité propre "
                "à chacune. Le travail a porté sur une déclinaison de bannières Facebook au "
                "même gabarit graphique (typographie, palette, mise en page) pour que les quatre "
                "pages soient immédiatement reconnaissables comme faisant partie d'un même "
                "groupe, ainsi que sur un logo animé pour l'antenne radio, pensé pour ouvrir "
                "les contenus vidéo et les directs."
            ),
            featured=True,
            image_path=find_file("Bannière", "D5 RADIO"),
            video_path=find_file("", "Animation Logo D5 RADIO"),
        )
        if d5_project:
            self.add_gallery_images(d5_project, [
                (find_file("Bannière", "D5 TV"), "Bannière Facebook D5 TV"),
                (find_file("Bannière", "D5 MUSIC"), "Bannière Facebook D5 Music"),
                (find_file("Bannière", "D5 NEWS"), "Bannière Facebook D5 News"),
                (find_file("Bannière", "D5 RADIO"), "Bannière Facebook D5 Radio"),
            ])

        # ------------------------------------------------------------------
        # 2. MYCOMEDY — bannière Facebook
        # ------------------------------------------------------------------
        self.upsert_project(
            title="Bannière Facebook MYCOMEDY",
            category=self.category("Design graphique"),
            services=[s for s in [design_service] if s],
            excerpt="Bannière Facebook pour la page humour MYCOMEDY.",
            description=(
                "Création d'une bannière Facebook pour la page MYCOMEDY, conçue pour capter "
                "l'attention dans un fil d'actualité chargé : composition simple, contraste fort "
                "et ton visuel qui reflète l'univers humoristique de la page."
            ),
            image_path=find_file("Bannière", "MYCOMEDY"),
        )

        # ------------------------------------------------------------------
        # 3-8. TOP CLIPS — habillages d'émission par genre/pays
        # ------------------------------------------------------------------
        top_clips_items = [
            ("TOP 10 MBALAX — Émission musicale", "AFFICHE TOP 10 MBALAX", "INTRO TOP 10 MBALAX", True,
             "affiche et générique d'intro pour le classement mbalax, pensés pour un public "
             "attaché aux codes visuels de cette scène musicale."),
            ("TOP 10 NAIJA — Émission musicale", "AFFICHE TOP 10 NAIJA", "NAIJA", True,
             "déclinaison de l'habillage Top Clips pour le classement naija, avec une affiche "
             "et un générique adaptés à l'identité de cette scène musicale."),
            ("TOP 10 Clips Rap France — Habillage émission", None, "RAP FRANCE", False,
             "version rap français de l'habillage Top Clips, montée pour donner le ton dès les "
             "premières secondes du classement."),
            ("TOP 10 Clips Rap US — Habillage émission", None, "RAP US", False,
             "déclinaison rap US de l'habillage Top Clips, avec un montage calé sur les codes "
             "visuels de cette scène."),
            ("TOP 10 Clips Pop & RnB France — Habillage émission", None, "POP & RNB FRANCE", False,
             "version pop & RnB français de l'habillage Top Clips, au ton plus feutré que les "
             "déclinaisons rap."),
            ("TOP 10 Clips Pop & RnB US — Habillage émission", None, "POP & RNB US", False,
             "déclinaison pop & RnB US de l'habillage Top Clips, avec la même structure de "
             "générique adaptée à l'ambiance du genre."),
        ]
        for title, banner_key, video_key, featured, detail in top_clips_items:
            self.upsert_project(
                title=title,
                category=category,
                client=top_clips,
                services=[s for s in [service] if s],
                excerpt=f"Habillage d'émission — {title.split(' — ')[0]}.",
                description=(
                    "Top Clips est un format de classement musical décliné par genre et par "
                    f"pays ; chaque édition garde la même structure de générique mais adapte "
                    f"le rythme et l'image au public visé. Cette version : {detail} "
                    "Le montage est calé sur le tempo de l'émission pour identifier "
                    "immédiatement le classement dès l'ouverture."
                ),
                featured=featured,
                image_path=find_file("Bannière", banner_key) if banner_key else None,
                video_path=find_file("Top Clips", video_key),
            )

        self.upsert_project(
            title="Sous-titrage animé — Top Clips",
            category=category,
            client=top_clips,
            services=[s for s in [service] if s],
            excerpt="Template de sous-titrage animé pour la série Top Clips.",
            description=(
                "Habillage de sous-titrage animé conçu pour être réutilisé sur l'ensemble des "
                "éditions Top Clips (Mbalax, Naija, Rap, Pop & RnB), afin de garder une "
                "cohérence visuelle d'un épisode à l'autre quel que soit le genre musical mis "
                "en avant."
            ),
            video_path=find_file("Top Clips", "Sous Titre Clips"),
        )

        # ------------------------------------------------------------------
        # 9-10. IDF TV
        # ------------------------------------------------------------------
        self.upsert_project(
            title="IDF TV — Habillage de chaîne",
            category=category,
            client=idf_tv,
            services=[s for s in [service] if s],
            excerpt="Identité de chaîne animée pour IDF TV.",
            description=(
                "Animation d'habillage pour la chaîne IDF TV : une identité visuelle en "
                "mouvement destinée à ouvrir les programmes et rappeler la marque de l'antenne "
                "sur l'ensemble de ses contenus, dans un format court pensé pour être diffusé "
                "en boucle sans lasser."
            ),
            featured=True,
            video_path=find_file("IDF", "Anim IDF"),
        )
        self.upsert_project(
            title="IDF TV — Spot publicitaire",
            category=category,
            client=idf_tv,
            services=[s for s in [video_service] if s],
            excerpt="Montage d'un spot publicitaire pour IDF TV.",
            description=(
                "Montage et habillage d'un spot publicitaire diffusé sur IDF TV : un exercice "
                "différent de l'habillage de chaîne, avec un message commercial à faire passer "
                "dans un format court, sans perdre en clarté ni en rythme."
            ),
            video_path=find_file("IDF", "PUB IDFTV"),
        )

        # ------------------------------------------------------------------
        # 11-12. Val-d'Oise TV
        # ------------------------------------------------------------------
        self.upsert_project(
            title="Val-d'Oise TV — Habillage de chaîne",
            category=category,
            client=val_doise_tv,
            services=[s for s in [service] if s],
            excerpt="Identité de chaîne animée pour Val-d'Oise TV.",
            description=(
                "Animation d'habillage pour Val-d'Oise TV, réalisée sur le même principe que "
                "pour IDF TV : une signature en mouvement courte et reconnaissable, conçue pour "
                "ouvrir les programmes de l'antenne locale."
            ),
            video_path=find_file("Val-D'oise", "Anim Val D"),
        )
        self.upsert_project(
            title="Val-d'Oise TV — Spot publicitaire",
            category=category,
            client=val_doise_tv,
            services=[s for s in [video_service] if s],
            excerpt="Montage d'un spot publicitaire pour Val-d'Oise TV.",
            description=(
                "Montage et habillage d'un spot publicitaire diffusé sur Val-d'Oise TV, avec un "
                "rythme de coupe pensé pour un format publicitaire court."
            ),
            video_path=find_file("Val-D'oise", "PUB VAL"),
        )

        # ------------------------------------------------------------------
        # 13-16. Habillages divers
        # ------------------------------------------------------------------
        self.upsert_project(
            title="Habillage Clips Internationaux",
            category=category,
            services=[s for s in [service] if s],
            excerpt="Générique d'intro pour une émission de clips internationaux.",
            description=(
                "Générique d'introduction animé conçu pour une émission consacrée aux clips "
                "internationaux : un habillage neutre en termes de scène musicale, capable "
                "d'introduire des sélections très variées sans imposer un univers graphique "
                "trop marqué."
            ),
            video_path=find_file("", "INTRO CLIPS INTERNATIONAUX"),
        )
        self.upsert_project(
            title="Habillage Podcast",
            category=category,
            services=[s for s in [service] if s],
            excerpt="Introduction animée pour un format podcast.",
            description=(
                "Introduction animée conçue pour ouvrir un format podcast : un habillage plus "
                "sobre que pour la télévision, pensé pour un public qui écoute autant qu'il "
                "regarde."
            ),
            video_path=find_file("", "PODCAST"),
        )
        self.upsert_project(
            title="Motion Design — Habillage animé",
            category=category,
            services=[s for s in [service] if s],
            excerpt="Composition de motion design libre, hors commande client.",
            description=(
                "Composition animée réalisée en dehors de toute commande client, pour explorer "
                "librement des mouvements, des transitions et des rythmes d'animation. Ce type "
                "de pièce sert de terrain d'essai avant de réutiliser certaines idées sur des "
                "projets clients."
            ),
            video_path=find_file("", "Anim Pro"),
        )
        self.upsert_project(
            title="Templates de titrage animé",
            category=category,
            services=[s for s in [service] if s],
            excerpt="Templates de titrage et sous-titrage réutilisables.",
            description=(
                "Ensemble de templates de titrage et de sous-titrage animés, conçus pour être "
                "réutilisés d'un projet à l'autre plutôt que refaits à chaque fois : une base "
                "qui accélère le montage tout en gardant un rendu cohérent."
            ),
            video_path=find_file("Titres", "Composition 1"),
        )

        # ------------------------------------------------------------------
        # 17. Showreel personnel (fichier trop volumineux pour être hébergé tel quel)
        # ------------------------------------------------------------------
        self.upsert_project(
            title="Showreel — Montage de clips musicaux",
            category=self.category("Montage vidéo"),
            services=[s for s in [video_service] if s],
            excerpt="Bobine démo de montage de clips musicaux.",
            description=(
                "Bobine démo personnelle rassemblant plusieurs montages de clips musicaux : "
                "choix des coupes, rythme calé sur la musique, transitions et effets visuels. "
                "Le fichier source (export brut, environ 395 Mo) n'a pas été mis en ligne "
                "directement pour ne pas alourdir le site ; une version compressée sera "
                "publiée ici."
            ),
            video_path=None,
            thumbnail_source_video=find_file("", "MONTAGE CLIPS"),
        )

        # ------------------------------------------------------------------
        # 18-19. Showreels du site (mis en avant sur la page d'accueil)
        # ------------------------------------------------------------------
        self.upsert_project(
            title="Showreel — Création Digitale",
            category=self.category("Web design"),
            services=[s for s in [design_service] if s],
            excerpt="Bobine de démonstration des créations digitales.",
            description=(
                "Bobine de démonstration qui rassemble des créations digitales réalisées pour "
                "différents clients : visuels de marque, bannières et contenus pensés pour les "
                "réseaux sociaux. Elle donne un aperçu rapide de l'étendue du travail de "
                "création visuelle, au-delà des projets présentés individuellement dans le "
                "portfolio."
            ),
            featured=True,
            video_path=find_file("", "Digital Site"),
        )
        self.upsert_project(
            title="Showreel — Audiovisuel & Montage",
            category=self.category("Montage vidéo"),
            services=[s for s in [video_service] if s],
            excerpt="Bobine de démonstration montage et habillage vidéo.",
            description=(
                "Bobine de démonstration centrée sur le montage et l'habillage vidéo : extraits "
                "d'habillages de chaîne, de génériques d'émission et de montages, choisis pour "
                "donner une vue d'ensemble du savoir-faire audiovisuel en quelques minutes."
            ),
            featured=True,
            video_path=find_file("", "Audiovisuel Site"),
        )

        self.stdout.write(self.style.SUCCESS("Bibliothèque de médias réels importée avec succès."))

    # ----------------------------------------------------------------------
    def category(self, name):
        return Category.objects.update_or_create(slug=slugify(name), defaults={"name": name})[0]

    def service(self, title, description, order):
        return Service.objects.update_or_create(
            slug=slugify(title),
            defaults={"title": title, "description": description, "order": order, "published": True, "icon": "bi-badge-tm"},
        )[0]

    def client(self, name):
        return Client.objects.update_or_create(name=name, defaults={})[0]

    def upsert_project(self, *, title, category, description, excerpt=None, services=None,
                        client=None, featured=False, image_path=None, video_path=None,
                        thumbnail_source_video=None):
        slug = slugify(title)
        project, _ = Project.objects.update_or_create(
            slug=slug,
            defaults={
                "title": title,
                "category": category,
                "client": client,
                "excerpt": excerpt or description,
                "description": description,
                "year": 2026,
                "featured": featured,
                "published": True,
            },
        )
        if services:
            project.services.set(services)

        if not project.thumbnail:
            if image_path and image_path.exists():
                self.attach_image_thumbnail(project, image_path)
            elif video_path and video_path.exists():
                self.attach_video_thumbnail(project, video_path)
            elif thumbnail_source_video and thumbnail_source_video.exists():
                self.attach_video_thumbnail(project, thumbnail_source_video)

        if video_path and video_path.exists() and not project.video_file:
            if video_path.stat().st_size <= MAX_VIDEO_BYTES:
                with open(video_path, "rb") as fh:
                    project.video_file.save(f"{slug}.mp4", ContentFile(fh.read()), save=True)

        return project

    def add_gallery_images(self, project, images):
        for order, (path, caption) in enumerate(images, start=1):
            if not path or not path.exists():
                continue
            if ProjectImage.objects.filter(project=project, caption=caption).exists():
                continue
            data = self.compress_png(path)
            image = ProjectImage(project=project, caption=caption, order=order)
            image.image.save(f"{project.slug}-{order}.png", ContentFile(data), save=True)

    def attach_image_thumbnail(self, project, path):
        data = self.compress_png(path)
        project.thumbnail.save(f"{project.slug}.png", ContentFile(data), save=True)

    def attach_video_thumbnail(self, project, path):
        frame_bytes = self.extract_video_frame(path)
        if frame_bytes:
            project.thumbnail.save(f"{project.slug}.jpg", ContentFile(frame_bytes), save=True)

    def compress_png(self, path, max_width=1600):
        try:
            image = Image.open(path)
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA")
            if image.width > max_width:
                ratio = max_width / float(image.width)
                image = image.resize((max_width, int(image.height * ratio)), Image.LANCZOS)
            buffer = io.BytesIO()
            image.save(buffer, format="PNG", optimize=True)
            return buffer.getvalue()
        except Exception:
            with open(path, "rb") as fh:
                return fh.read()

    def extract_video_frame(self, path, seek_ratio=0.15, max_width=1280):
        try:
            cap = cv2.VideoCapture(str(path))
            if not cap.isOpened():
                return None
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
            target_frame = int(frame_count * seek_ratio) if frame_count > 1 else 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ok, frame = cap.read()
            if not ok:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ok, frame = cap.read()
            cap.release()
            if not ok or frame is None:
                return None

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            if image.width > max_width:
                ratio = max_width / float(image.width)
                image = image.resize((max_width, int(image.height * ratio)), Image.LANCZOS)
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=82, optimize=True)
            return buffer.getvalue()
        except Exception:
            return None
