from django.shortcuts import render

from .models import Profile, AboutSettings


def about_view(request):
    return render(request, "about_me/about.html", {
        "profile": Profile.load(),
        "about_settings": AboutSettings.objects.first(),
    })
