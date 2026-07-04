from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

from about_me.views import about_view
from contact.views import contact_thanks, contact_view, devis_view
from core.sitemaps import PostSitemap, ProjectSitemap, ServiceSitemap, StaticViewSitemap
from core.views import robots_txt
from projects.views import gallery_view, project_detail, project_list

sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "services": ServiceSitemap,
    "blog": PostSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),
    path("", include("core.urls")),
    path("realisations/", project_list, name="realisations"),
    path("realisations/<slug:slug>/", project_detail, name="realisation_detail"),
    path("galerie/", gallery_view, name="gallery"),
    path("portfolio/", project_list, name="project_list"),
    path("portfolio/<slug:slug>/", project_detail, name="project_detail"),
    path("projects/", include("projects.urls")),
    path("about/", about_view, name="about"),
    path("about/", include("about_me.urls")),
    path("contact/", contact_view, name="contact"),
    path("contact/thanks/", contact_thanks, name="contact_thanks"),
    path("contact/", include("contact.urls")),
    path("devis/", devis_view, name="devis"),
    path("services/", include("services.urls")),
    path("blog/", include("blog.urls")),
    path("temoignages/", include("testimonials.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]

urlpatterns += debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
