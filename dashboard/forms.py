from django import forms
from projects.models import Project, ProjectImage, Skill
from blog.models import Post
from services.models import Service
from contact.models import Message
from core.models import SiteSettings
from django.contrib.auth.forms import SetPasswordForm

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '••••••••',
            'id': 'new_password1'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': '••••••••',
            'id': 'new_password2'
        })


def bootstrapify(form):
    for name, field in form.fields.items():
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.setdefault("class", "form-check-input")
        elif isinstance(field.widget, (forms.CheckboxSelectMultiple, forms.RadioSelect)):
            continue
        elif isinstance(field.widget, forms.Select):
            field.widget.attrs.setdefault("class", "form-select")
        else:
            field.widget.attrs.setdefault("class", "form-control")
    return form


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title", "slug", "category", "client", "services",
            "excerpt", "description", "year",
            "thumbnail", "image", "video_url", "video_file", "live_url",
            "published", "featured",
        ]
        widgets = {"services": forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrapify(self)


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ["image", "caption", "order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrapify(self)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "slug", "excerpt", "content", "published", "categories", "tags"]
        widgets = {"categories": forms.CheckboxSelectMultiple, "tags": forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrapify(self)


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["title", "slug", "description", "icon", "order", "published"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bootstrapify(self)


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "level", "order"]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["is_read"]
        widgets = {"is_read": forms.CheckboxInput(attrs={"class": "form-check-input"})}


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ["site_title"]
