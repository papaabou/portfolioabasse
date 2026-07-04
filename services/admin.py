from django.contrib import admin
from .models import Service, Deliverable, ProcessStep
from django.contrib.contenttypes.admin import GenericTabularInline
from core.models import ContentBlock

class DeliverableInline(admin.TabularInline):
    model = Deliverable
    extra = 1
    fields = ("name", "order")
    ordering = ("order",)


class ProcessStepInline(admin.TabularInline):
    model = ProcessStep
    extra = 1
    fields = ("title", "description", "order")
    ordering = ("order",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "order")
    list_filter = ("published",)
    search_fields = ("title", "description")
    ordering = ("order",)
    prepopulated_fields = {"slug": ("title",)}

    inlines = [
        DeliverableInline,
        ProcessStepInline,
    ]


class ContentBlockInline(GenericTabularInline):
    model = ContentBlock
    extra = 1
    fields = ("block_type", "heading", "body", "image", "order")

ServiceAdmin.inlines = ServiceAdmin.inlines + [ContentBlockInline]


@admin.register(Deliverable)
class DeliverableAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "order")
    list_filter = ("service",)
    search_fields = ("name",)
    ordering = ("order",)


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("title", "service", "order")
    list_filter = ("service",)
    search_fields = ("title", "description")
    ordering = ("order",)
