from django.contrib import admin
from .models import Message
from .models import ContactSettings
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "is_read", "created")
    list_filter = ("is_read",)
    readonly_fields = ("name", "email", "service", "budget", "body", "created")
    actions = ["mark_as_read"]

    def has_add_permission(self, request):
        return False

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"Marked {updated} message(s) as read.")

    mark_as_read.short_description = "Mark selected messages as read"

@admin.register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):
    list_display = ("sender_name",)

    def has_add_permission(self, request):
        return not ContactSettings.objects.exists()