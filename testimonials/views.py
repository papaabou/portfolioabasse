from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from portfolio_site.utils import render_thanks
from .models import Testimonial, TestimonialPageSettings
from .forms import TestimonialSubmissionForm
from projects.models import Project
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from contact.models import ContactSettings
from about_me.models import Profile
from portfolio_site.utils import send_django_email_async

def testimonials_list(request):
    qs = Testimonial.objects.filter(approved=True).order_by("-featured", "order")
    paginator = Paginator(qs, 6)
    page = request.GET.get("page")
    items = paginator.get_page(page)
    return render(request, "testimonials/testimonial_list.html", {"testimonials": items})

def testimonial_submit(request):
    project = None
    project_slug = request.GET.get("project")

    if project_slug:
        project = get_object_or_404(Project, slug=project_slug, published=True)

    form_config = {
        "name": {
            "label": "Nom complet",
            "placeholder": "Jeanne Dupont",
        },
        "company": {
            "label": "Entreprise (optionnel)",
            "placeholder": "Nom de votre entreprise",
        },
        "email": {
            "label": "Email (ne sera pas publié)",
            "placeholder": "vous@exemple.com",
        },
        "role": {
            "label": "Fonction (optionnel)",
            "placeholder": "Fondatrice, Responsable marketing...",
        },
        "rating": {
            "label": "Votre note",
            "help_text": "1 = Décevant, 5 = Excellent",
        },
        "body": {
            "label": "Votre témoignage",
            "placeholder": "Décrivez votre expérience avec Abasse : le projet, le résultat, ce que vous avez apprécié...",
        },
    }

    if request.method == "POST":
        form = TestimonialSubmissionForm(request.POST, project=project, config=form_config,)
        if form.is_valid():
            testimonial = form.save()

            # ContactSettings.recipient_email is the address explicitly chosen
            # to receive notifications. Fall back to the Profile owner's email,
            # then to the site's default sender, only if it isn't set.
            profile = Profile.load()
            sender_name = profile.full_name if profile and profile.full_name else "Abasse NIANG"

            settings_obj = ContactSettings.objects.first()
            recipient_email = (
                getattr(settings_obj, "recipient_email", None)
                or (profile.email if profile and profile.email else None)
                or settings.RESEND_FROM_EMAIL
            )

            # =============================
            # 1️⃣ ADMIN NOTIFICATION
            # =============================
            subject_admin = (
                f"Nouveau témoignage — {testimonial.project.title}"
                if testimonial.project
                else "Nouveau témoignage reçu"
            )

            context_admin = {
                "testimonial": testimonial,
                "project": testimonial.project,
            }

            text_admin = render_to_string(
                "emails/testimonial_notification.txt", context_admin
            )
            html_admin = render_to_string(
                "emails/testimonial_notification.html", context_admin
            )

            send_django_email_async(
                subject=subject_admin,
                to=[recipient_email],
                text=text_admin,
                html=html_admin,
                reply_to=testimonial.email,
                sender_name=sender_name,
            )

            # =============================
            # 2️⃣ AUTO-REPLY TO SUBMITTER
            # =============================
            if testimonial.email:
                subject_user = "Merci pour votre témoignage !"
                context_user = {
                    "testimonial": testimonial,
                    "project": testimonial.project,
                }

                text_user = render_to_string(
                    "emails/testimonial_autoreply.txt", context_user
                )
                html_user = render_to_string(
                    "emails/testimonial_autoreply.html", context_user
                )

                send_django_email_async(
                    subject=subject_user,
                    to=[testimonial.email],
                    text=text_user,
                    html=html_user,
                    sender_name=sender_name,
                )

            request.session["testimonial_submitted"] = True

            if not project_slug:
                form_project = form.cleaned_data.get("project")
                if form_project:
                    project_slug = form_project.slug
                    request.session["project"] = project_slug

            if project_slug:
                return redirect(
                    f"{reverse('testimonial_thanks')}?project={project_slug}"
                )
            return redirect("testimonial_thanks")
    else:
        form = TestimonialSubmissionForm(project=project, config=form_config,)

    page_settings = TestimonialPageSettings.objects.first()
    return render(
        request,
        "testimonials/testimonial_submit.html",
        {
            "form": form,
            "project": project,
            "page_settings": page_settings,
            "show_footer_contact": False,
        },
    )

def testimonial_thanks(request):
    page_settings = TestimonialPageSettings.objects.first()
    project_slug = request.GET.get("project") or request.session.get("project")
    project = None
    if project_slug:
        project = get_object_or_404(Project, slug=project_slug, published=True)

    if request.session.get("project"):
        del request.session["project"]

    return render_thanks(
        request,
        session_key="testimonial_submitted",
        redirect_url="testimonials_list",
        extra_context={
            "show_footer_contact": True,
            "title": page_settings.thanks_title if page_settings else f"Thank You{f' – {project.title}' if project else ''}",
            "heading": page_settings.thanks_title if page_settings else "Thank You for Your Testimonial",
            "subheading": page_settings.thanks_subheading if page_settings else "Testimonial Received",
            "message": page_settings.thanks_message if page_settings else "Your testimonial has been received and will appear on the site after approval.",
            "project": project,
        },
    )
