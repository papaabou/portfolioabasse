from django.db import models
from services.models import Service

PROJECT_TYPE_CHOICES = [
    ("visuels", "Création visuelle"),
    ("video", "Montage vidéo"),
    ("thumbnail", "Miniatures YouTube"),
    ("branding", "Charte graphique"),
    ("web", "Web design"),
    ("photo", "Photo"),
    ("autre", "Autre"),
]

DEADLINE_CHOICES = [
    ("urgent", "Urgent (moins d'une semaine)"),
    ("2_4_semaines", "2 à 4 semaines"),
    ("1_3_mois", "1 à 3 mois"),
    ("flexible", "Flexible / pas de date précise"),
]


class Message(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    project_type = models.CharField(max_length=30, choices=PROJECT_TYPE_CHOICES, blank=True)
    budget = models.DecimalField(
        max_digits=10,  # total digits
        decimal_places=2,  # digits after decimal
        null=True,
        blank=True,
        help_text="Budget estimé en euros (EUR)"
    )
    deadline = models.CharField(max_length=30, choices=DEADLINE_CHOICES, blank=True)
    body = models.TextField()
    is_quote_request = models.BooleanField(default=False, help_text="Coché si le message vient du formulaire de devis")
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Message from {self.name}"

class ContactSettings(models.Model):
    sender_name = models.CharField(
        max_length=100,
        default="Abasse NIANG",
        help_text="Nom affiché comme expéditeur dans les emails automatiques"
    )
    recipient_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Adresse qui reçoit une copie de chaque message/devis. Laisser vide pour utiliser l'email du profil.",
    )
    sender_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Contact Settings: {self.sender_email or '(non défini)'} → {self.recipient_email or '(non défini)'}"

    class Meta:
        verbose_name = "Contact Settings"
        verbose_name_plural = "Contact Settings"