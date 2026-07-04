from django.contrib import admin
from .models import FAQItem, SiteSettings
from .models import ContentBlock
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "published")
    list_editable = ("order", "published")
    search_fields = ("question", "answer")


class ContentBlockInline(GenericTabularInline):
    model = ContentBlock
    extra = 1
    fields = ("block_type", "heading", "body", "image", "order")


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ("__str__", "content_type", "object_id", "block_type", "order")
    list_filter = ("block_type", "content_type")

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    fieldsets = (
        ("Site Info / Favicon", {
            "fields": ("site_title", "tagline", "logo", "favicon")
        }),
        ("Footer / About", {
            "fields": ("about_short", "footer_text")
        }),
        ("SEO / Social Preview", {
            "fields": (
                "meta_title",
                "meta_description",
                "og_title",
                "og_description",
                "og_image",
                "twitter_card"
            )
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True
