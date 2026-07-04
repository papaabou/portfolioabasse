from datetime import date

from django.core.management.base import BaseCommand

from about_me.models import AboutSettings, CoreValue, Journey, Profile
from projects.models import Skill


class Command(BaseCommand):
    help = "Enrich the profile (bio, contact, skills, career) with real data from Abasse's CV."

    def handle(self, *args, **options):
        profile = Profile.load()
        profile.full_name = "Abasse NIANG"
        profile.email = "bassitniang1998@gmail.com"
        profile.phone = "+33 7 45 60 79 64"
        profile.whatsapp = "33745607964"
        profile.career_start_date = date(2018, 1, 1)
        profile.short_bio = (
            "Réalisateur, vidéaste et monteur vidéo basé à Créteil, je crée des contenus "
            "visuels dynamiques et engageants. Motivé, polyvalent et rigoureux, je suis à "
            "l'aise à toutes les étapes de la production audiovisuelle : tournage, montage, "
            "motion design et habillage."
        )
        profile.save()

        skills = [
            ("Montage vidéo (Premiere Pro)", 95, 1),
            ("Motion design (After Effects)", 90, 2),
            ("Retouche photo (Photoshop)", 88, 3),
            ("Étalonnage (DaVinci Resolve)", 82, 4),
            ("Habillage TV & régie (vMix)", 85, 5),
            ("Design graphique (Illustrator)", 85, 6),
            ("Mise en page (InDesign)", 75, 7),
            ("Prototypage web (Figma)", 75, 8),
            ("Web (HTML, CSS, WordPress)", 65, 9),
        ]
        skill_objs = []
        for name, level, order in skills:
            skill, _ = Skill.objects.update_or_create(
                name=name, defaults={"level": level, "order": order}
            )
            skill_objs.append(skill)
        profile.skills.set(skill_objs)

        journeys = [
            {
                "title": "Réalisateur et Monteur Vidéo / Motion Designer — XKSGROUP, Paris (alternance)",
                "description": "Tournage, réalisation, programmation régie et montage vidéo. "
                                "Création d'habillages TV (intro, broadcast, logos, titres) et "
                                "de chartes graphiques, logos, bannières.",
                "start_year": "2025",
                "end_year": "en cours",
                "order": 1,
            },
            {
                "title": "Monteur Vidéo — Graines de Réussite, Paris (alternance)",
                "description": "Réalisation et montage de vidéos de formation (cartes mentales, "
                                "lecture rapide, gestion du stress) pour la plateforme de "
                                "l'entreprise. Montage de vidéos longues et courtes pour les "
                                "réseaux sociaux, création d'animations.",
                "start_year": "2024",
                "end_year": "2025",
                "order": 2,
            },
            {
                "title": "Graphiste et Monteur Vidéo — Pangée ONG, Paris (stage)",
                "description": "Conception des visuels et mise en page de maquettes de site web. "
                                "Montage vidéo pour les réseaux sociaux et création d'animations "
                                "(titres, logos).",
                "start_year": "2024",
                "end_year": "2024",
                "order": 3,
            },
            {
                "title": "Cadreur et Monteur Vidéo — Baadoola TV, Dakar (CDD)",
                "description": "Production (tournage), post-production (dérushage, montage, "
                                "étalonnage), création d'animations (titres, logos, génériques) "
                                "et diffusion sur les réseaux sociaux.",
                "start_year": "2021",
                "end_year": "2023",
                "order": 4,
            },
            {
                "title": "Infographiste — Fanthio multiservices (CDD)",
                "description": "Conception de logos, affiches, chartes graphiques, étiquettes de "
                                "vente, cartes de visite et maquettes de site web/application.",
                "start_year": "2018",
                "end_year": "2019",
                "order": 5,
            },
            {
                "title": "Photographe et vidéaste — Lachica.fr (e-commerce)",
                "description": "Photographie et vidéo produit pour un site e-commerce.",
                "start_year": "2018",
                "end_year": "2019",
                "order": 6,
            },
        ]
        for data in journeys:
            Journey.objects.update_or_create(
                profile=profile,
                title=data["title"],
                defaults={
                    "description": data["description"],
                    "start_year": data["start_year"],
                    "end_year": data["end_year"],
                    "order": data["order"],
                },
            )

        values = ["Forte motivation", "Ponctualité", "Travail d'équipe", "Créativité", "Curiosité"]
        for order, title in enumerate(values, start=1):
            CoreValue.objects.update_or_create(
                profile=profile, title=title, defaults={"order": order}
            )

        AboutSettings.objects.update_or_create(
            pk=1,
            defaults={
                "hero_title": "Réalisateur · Vidéaste · Monteur vidéo",
                "hero_subtitle": (
                    "À la recherche d'un contrat à durée indéterminée (CDI) à partir de "
                    "septembre 2026, au sein d'une équipe créative."
                ),
                "meta_title": "Abasse NIANG — Réalisateur, Vidéaste, Monteur vidéo",
                "meta_description": (
                    "Abasse NIANG, réalisateur, vidéaste et monteur vidéo basé à Créteil. "
                    "À la recherche d'un CDI à partir de septembre 2026."
                ),
            },
        )

        self.stdout.write(self.style.SUCCESS("Profil enrichi avec les donnees du CV."))
