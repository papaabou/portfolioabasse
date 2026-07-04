from django.contrib import admin
from .models import Testimonial, TestimonialPageSettings
from django.contrib.contenttypes.admin import GenericTabularInline
from core.models import ContentBlock

@admin.register(TestimonialPageSettings)
class TestimonialPageSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance
        return not TestimonialPageSettings.objects.exists()


class ContentBlockInline(GenericTabularInline):
    model = ContentBlock
    extra = 1
    fields = ("block_type", "heading", "body", "image", "order")

TestimonialPageSettingsAdmin.inlines = [ContentBlockInline]

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "project","approved",)
    list_filter = ("approved","created", "featured","rating",)
    search_fields = ("name","company","role","body",)
    ordering = ("-featured", "order",)
    list_editable = ("approved",)
    readonly_fields = ("name","client", "email", "company","role","project","body",)
    actions = ["approve_testimonials", "decline_testimonials"]

    def has_add_permission(self, request):
        return False

    def approve_testimonials(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"Approved {updated} testimonial(s)")

    def decline_testimonials(self, request, queryset):
        updated = queryset.update(approved=False)
        self.message_user(request, f"Declined {updated} testimonial(s)")

    approve_testimonials.short_description = "Approve selected testimonials"
    decline_testimonials.short_description = "Decline selected testimonials"
