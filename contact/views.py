from django.shortcuts import render, redirect

from about_me.models import Profile
from portfolio_site.utils import render_thanks
from .forms import CONTACT_FIELD_CONFIG, ContactForm, DevisForm
from .services import handle_contact_submission


def contact_view(request):
    profile = Profile.load()
    sent = False

    if request.method == "POST":
        form = ContactForm(request.POST, config=CONTACT_FIELD_CONFIG)
        if form.is_valid():
            handle_contact_submission(
                form=form,
                request=request,
                admin_subject=f"Nouveau message de {form.cleaned_data['name']}",
                admin_templates={
                    "text": "emails/contact_notification.txt",
                    "html": "emails/contact_notification.html",
                },
                user_subject="Votre message a bien été reçu",
                user_templates={
                    "text": "emails/contact_autoreply.txt",
                    "html": "emails/contact_autoreply.html",
                },
            )
            sent = True
            form = ContactForm(config=CONTACT_FIELD_CONFIG)
    else:
        form = ContactForm(config=CONTACT_FIELD_CONFIG)

    return render(request, "contact/contact.html", {
        "form": form,
        "profile": profile,
        "sent": sent,
    })


def devis_view(request):
    profile = Profile.load()
    sent = False

    if request.method == "POST":
        form = DevisForm(request.POST)
        if form.is_valid():
            handle_contact_submission(
                form=form,
                request=request,
                admin_subject=f"Nouvelle demande de devis de {form.cleaned_data['name']}",
                admin_templates={
                    "text": "emails/contact_notification.txt",
                    "html": "emails/contact_notification.html",
                },
                user_subject="Votre demande de devis a bien été reçue",
                user_templates={
                    "text": "emails/contact_autoreply.txt",
                    "html": "emails/contact_autoreply.html",
                },
            )
            sent = True
            form = DevisForm()
    else:
        form = DevisForm()

    return render(request, "contact/devis.html", {
        "form": form,
        "profile": profile,
        "sent": sent,
    })


def contact_thanks(request):
    return render_thanks(
        request,
        session_key="form_submitted",
        redirect_url="contact",
        extra_context={"show_footer_contact": True},
    )
