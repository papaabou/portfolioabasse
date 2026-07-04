from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator

from about_me.models import Profile
from contact.services import handle_contact_submission
from .forms import ServiceContactForm
from .models import Service


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, published=True)

    if request.method == "POST":
        form = ServiceContactForm(request.POST, service=service)
        if form.is_valid():
            form.instance.service = service
            form.instance.is_quote_request = True
            handle_contact_submission(
                form=form,
                request=request,
                admin_subject=f"Nouvelle demande pour « {service.title} » — {form.cleaned_data['name']}",
                admin_templates={
                    "text": "emails/contact_notification.txt",
                    "html": "emails/contact_notification.html",
                },
                user_subject="Votre demande a bien été reçue",
                user_templates={
                    "text": "emails/contact_autoreply.txt",
                    "html": "emails/contact_autoreply.html",
                },
            )
            return redirect("contact_thanks")
    else:
        form = ServiceContactForm(service=service)

    return render(request, "services/service_detail.html", {
        "service": service,
        "form": form,
        "show_footer_contact": False,
    })


def service_list(request):
    qs = Service.objects.filter(published=True).prefetch_related("projects")
    paginator = Paginator(qs, 9)
    page = request.GET.get("page")
    services = paginator.get_page(page)
    profile = Profile.load()
    for service in services:
        service.sample_project = next(
            (p for p in service.projects.all() if p.published and p.cover_image),
            None,
        )
        service.sample_image_url = None
        if service.sample_project:
            service.sample_image_url = service.sample_project.cover_image.url
        elif service.slug == "photo" and profile and profile.profile_image:
            service.sample_image_url = profile.profile_image.url
    return render(request, "services/services_list.html", {"services": services})
