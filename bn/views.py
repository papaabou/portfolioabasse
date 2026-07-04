from django.shortcuts import render, get_object_or_404, redirect
from .models import BNAboutPage
from projects.models import Project
from about_me.models import Profile
from contact.forms import ContactForm
from contact.services import handle_contact_submission

def about(request):
    page = get_object_or_404(BNAboutPage)
    project_count = Project.objects.count()
    profile = Profile.load()

    # Bangla form configuration
    form_config = {
        "_remove": ["budget"],

        "name": {
            "label": "আপনার নাম",
            "placeholder": "যেমন: ওসামা আবদুল্লাহ",
        },
        "email": {
            "label": "ইমেইল এড্রেস",
            "placeholder": "email@example.com",
        },
        "service": {
            "label": "আপনার প্রজেক্টের ধরন",
            "placeholder": "যেমন: থিম কাস্টমাইজেশন বা বাগ ফিক্স",
        },
        "body": {
            "label": "বিস্তারিত মেসেজ",
            "placeholder": "আপনার প্রজেক্টের বিস্তারিত এখানে লিখুন...",
        },
    }

    if request.method == "POST":
        form = ContactForm(request.POST, config=form_config)
        if form.is_valid():
            handle_contact_submission(
                form=form,
                request=request,
                admin_subject="নতুন প্রজেক্ট ইনকোয়ারি (About Page)",
                admin_templates={
                    "text": "emails/contact_notification.txt",
                    "html": "emails/contact_notification.html",
                },
                user_subject="ধন্যবাদ! আপনার মেসেজ পেয়েছি",
                user_templates={
                    "text": "emails/contact_autoreply.txt",
                    "html": "emails/contact_autoreply.html",
                },
            )
            return redirect("contact_thanks")
    else:
        form = ContactForm(config=form_config)

    context = {
        "page": page,
        "project_count": project_count,
        "profile": profile,
        "form": form,
    }

    return render(request, "bn/about.html", context)
