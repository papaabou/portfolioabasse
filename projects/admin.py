from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Client, Project, ProjectImage, Skill


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "caption", "order")
    ordering = ("order",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("thumbnail_preview", "title", "category", "client", "year", "featured", "published")
    list_filter = ("published", "featured", "category", "year", "services")
    search_fields = ("title", "excerpt", "description", "client__name", "client__company_name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("services", "technologies")
    autocomplete_fields = ("category", "client")
    readonly_fields = ("thumbnail_preview_large",)
    list_editable = ("featured", "published")
    date_hierarchy = "created"
    inlines = (ProjectImageInline,)

    fieldsets = (
        ("Essentiel", {
            "fields": ("title", "slug", "category", "client", "year", "published", "featured")
        }),
        ("Contenu", {
            "fields": ("excerpt", "description", "services", "technologies")
        }),
        ("Images et video", {
            "fields": ("thumbnail_preview_large", "thumbnail", "image", "video_file", "video_url", "live_url")
        }),
        ("Referencement", {
            "classes": ("collapse",),
            "fields": ("seo_title", "seo_description", "seo_keywords")
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width:72px;height:52px;object-fit:cover;border-radius:6px;" />',
                obj.cover_image.url,
            )
        return "-"

    thumbnail_preview.short_description = "Apercu"

    def thumbnail_preview_large(self, obj):
        if obj and obj.cover_image:
            return format_html(
                '<img src="{}" style="width:320px;max-width:100%;height:auto;border-radius:8px;" />',
                obj.cover_image.url,
            )
        return "Ajoutez une image principale pour afficher un apercu."

    thumbnail_preview_large.short_description = "Apercu image"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company_name", "email", "whatsapp")
    search_fields = ("name", "company_name", "email")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "order")
    list_editable = ("level", "order")
    search_fields = ("name",)
    ordering = ("order", "name")


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "image_preview", "caption", "order")
    list_filter = ("project",)
    search_fields = ("caption", "project__title")
    ordering = ("order",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px;height:56px;object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Apercu"
