from django.contrib import admin
from .models import (
    BNAboutPage,
    BNPricingPlan,
    BNProcessStep,
    BNFAQ,
)


class BNPricingPlanInline(admin.TabularInline):
    model = BNPricingPlan
    extra = 1


class BNProcessStepInline(admin.TabularInline):
    model = BNProcessStep
    extra = 1
    ordering = ("order",)


class BNFAQInline(admin.TabularInline):
    model = BNFAQ
    extra = 1
    ordering = ("order",)


@admin.register(BNAboutPage)
class BNAboutPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Hero Section", {
            "fields": (
                "hero_badge_text",
                "hero_title",
                "hero_subtitle",
                "hero_video_url",
                "hero_cta_text",
                "hero_cta_link",
            )
        }),
        ("Services", {
            "fields": ("service_title", "service_subtitle", "services")
        }),
        ("Projects / Portfolio", {
            "fields": ("project_title", "project_subtitle", "projects")
        }),
        ("Pricing / Packages", {
            "fields": ("pricing_title", "pricing_subtitle")
        }),
        ("Experience", {
            "fields": ("experience_title", "experience_subtitle")
        }),
        ("Process Section", {
            "fields": ("process_title", "process_subtitle")
        }),
        ("Testimonials", {
            "fields": ("testimonial_title", "testimonial_subtitle", "testimonials")
        }),
        ("FAQ Section", {
            "fields": ("faq_title", "faq_subtitle")
        }),
        ("Meeting Scheduler", {
            "fields": ("meeting_title", "meeting_subtitle", "calendly_url")
        }),
        ("Contact Section", {
            "fields": ("contact_title", "contact_subtitle")
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description")
        }),
    )

    filter_horizontal = ("services", "projects", "testimonials")
    inlines = [
        BNPricingPlanInline,
        BNProcessStepInline,
        BNFAQInline,
    ]

    def has_add_permission(self, request):
        return not BNAboutPage.objects.exists()
