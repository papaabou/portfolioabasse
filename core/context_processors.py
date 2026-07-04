import time

from .models import SiteSettings
from about_me.models import Profile

STATIC_VERSION = str(int(time.time()))


def site_settings(request):
    try:
        settings = SiteSettings.load()
    except Exception:
        settings = None

    try:
        profile = Profile.load()
    except Exception:
        profile = Profile.objects.filter(is_active=True).first()

    social_links = profile.social_links.all() if profile else []

    return {
        "site_settings": settings,
        "profile": profile,
        "social_links": social_links,
        "static_version": STATIC_VERSION,
    }
