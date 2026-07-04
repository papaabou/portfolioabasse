from django.contrib import admin
from .models import Post, Category, Tag
from django.contrib.contenttypes.admin import GenericTabularInline
from core.models import ContentBlock


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published", "created")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "content")
    list_filter = ("published", "author")
    filter_horizontal = ("categories", "tags")
    inlines = []


class ContentBlockInline(GenericTabularInline):
    model = ContentBlock
    extra = 1
    fields = ("block_type", "heading", "body", "image", "order")

PostAdmin.inlines = [ContentBlockInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
