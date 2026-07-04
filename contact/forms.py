from django import forms
from services.models import Service
from .models import DEADLINE_CHOICES, PROJECT_TYPE_CHOICES, Message


CONTACT_FIELD_CONFIG = {
    "name": {"label": "Nom complet", "placeholder": "Votre nom"},
    "email": {"label": "Email", "placeholder": "vous@exemple.com"},
    "service": {"label": "Service concerné"},
    "budget": {"label": "Budget estimé (€)", "placeholder": "Ex : 500"},
    "body": {"label": "Votre message", "placeholder": "Décrivez votre projet..."},
}


def _apply_bootstrap_classes(fields):
    for field in fields.values():
        widget = field.widget
        if isinstance(widget, (forms.Select, forms.SelectMultiple)):
            widget.attrs.setdefault("class", "form-select")
        elif isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault("class", "form-check-input")
        else:
            widget.attrs.setdefault("class", "form-control")


class ContactForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(published=True),
        empty_label="Choisir un service (optionnel)",
        required=False,
    )

    class Meta:
        model = Message
        fields = ["name", "email", "service", "budget", "body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        config = kwargs.pop("config", {})
        super().__init__(*args, **kwargs)
        _apply_bootstrap_classes(self.fields)

        for field_name, field_config in config.items():
            if field_name not in self.fields:
                continue

            field = self.fields[field_name]

            if "label" in field_config:
                field.label = field_config["label"]

            if "help_text" in field_config:
                field.help_text = field_config["help_text"]

            if "placeholder" in field_config:
                field.widget.attrs["placeholder"] = field_config["placeholder"]

        remove_fields = config.get("_remove", [])
        for field_name in remove_fields:
            self.fields.pop(field_name, None)


class DevisForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(published=True),
        empty_label="Choisir un service (optionnel)",
        required=False,
        label="Service concerné",
    )
    project_type = forms.ChoiceField(
        choices=[("", "Choisir un type de projet")] + PROJECT_TYPE_CHOICES,
        required=False,
        label="Type de projet",
    )
    deadline = forms.ChoiceField(
        choices=[("", "Choisir un délai")] + DEADLINE_CHOICES,
        required=False,
        label="Délai souhaité",
    )

    class Meta:
        model = Message
        fields = ["name", "email", "phone", "project_type", "service", "budget", "deadline", "body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 6}),
        }
        labels = {
            "name": "Nom complet",
            "email": "Email",
            "phone": "Téléphone (optionnel)",
            "budget": "Budget estimé (€)",
            "body": "Décrivez votre projet",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_bootstrap_classes(self.fields)
        self.fields["name"].widget.attrs.setdefault("placeholder", "Votre nom")
        self.fields["email"].widget.attrs.setdefault("placeholder", "vous@exemple.com")
        self.fields["phone"].widget.attrs.setdefault("placeholder", "06 12 34 56 78")
        self.fields["budget"].widget.attrs.setdefault("placeholder", "Ex : 500")
        self.fields["body"].widget.attrs.setdefault(
            "placeholder",
            "Décrivez votre projet : objectif, support (vidéo, miniature, charte...), références, contraintes...",
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_quote_request = True
        if commit:
            instance.save()
        return instance
