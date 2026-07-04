from django.contrib import admin
from .models import Profile, Journey, CoreValue, AboutSettings, SocialLink
from django.contrib.contenttypes.admin import GenericTabularInline
from core.models import ContentBlock

class JourneyInline(admin.TabularInline):
    model = Journey
    extra = 1

class CoreValueInline(admin.TabularInline):
    model = CoreValue
    extra = 1

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    ordering = ("order",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "is_active", "email")
    filter_horizontal = ("skills",)
    inlines = [SocialLinkInline, JourneyInline, CoreValueInline]

    def has_add_permission(self, request):
        # enforce singleton: only allow create if none exists
        return not Profile.objects.exists()

@admin.register(AboutSettings)
class AboutSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # prevent creating multiple instances
        return not AboutSettings.objects.exists()


class ContentBlockInline(GenericTabularInline):
    model = ContentBlock
    extra = 1
    fields = ("block_type", "heading", "body", "image", "order")

AboutSettingsAdmin.inlines = [ContentBlockInline]