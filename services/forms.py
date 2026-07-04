from django import forms

from contact.forms import CONTACT_FIELD_CONFIG, ContactForm


class ServiceContactForm(ContactForm):
    def __init__(self, *args, **kwargs):
        service = kwargs.pop("service", None)
        kwargs.setdefault("config", CONTACT_FIELD_CONFIG)
        super().__init__(*args, **kwargs)
        if service:
            self.fields["service"].initial = service
        self.fields["service"].widget = forms.HiddenInput()
