from django import forms
from .models import Testimonial
from projects.models import Project
from projects.models import Client


class TestimonialSubmissionForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = [
            "name","email","company","role","rating","body","project",
        ]
        widgets = {
            "rating": forms.RadioSelect(),
            "body": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, project=None, config=None, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "rating":
                continue
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

        # ---------- CONFIG CONTROL (labels, placeholders, help text) ----------
        config = config or {}

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

        # ---------- PROJECT HANDLING ----------
        if project:
            self.fields["project"].widget = forms.HiddenInput()
            self.initial["project"] = project
        else:
            self.fields["project"].queryset = Project.objects.filter(published=True)
            self.fields["project"].required = False

    def save(self, commit=True):
        testimonial = super().save(commit=False)

        email = self.cleaned_data.get("email")
        if email:
            client, _ = Client.objects.get_or_create(
                email=email,
                defaults={
                    "name": self.cleaned_data["name"],
                    "company_name": self.cleaned_data.get("company", ""),
                },
            )
            testimonial.client = client

        if commit:
            testimonial.save()

        return testimonial
