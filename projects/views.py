from django.shortcuts import get_object_or_404, render

from .models import Category, Project, ProjectImage


def project_list(request):
    category_slug = request.GET.get("category")
    categories = Category.objects.filter(projects__published=True).distinct()
    projects = Project.objects.filter(published=True).select_related("category", "client").prefetch_related("services")

    if category_slug:
        projects = projects.filter(category__slug=category_slug)

    return render(request, "projects/project_list.html", {
        "projects": projects,
        "categories": categories,
        "current_category": category_slug,
    })


def gallery_view(request):
    category_slug = request.GET.get("category")
    categories = Category.objects.filter(projects__published=True).distinct()

    projects = Project.objects.filter(published=True).select_related("category")
    if category_slug:
        projects = projects.filter(category__slug=category_slug)

    extra_images = ProjectImage.objects.filter(project__published=True).select_related("project", "project__category")
    if category_slug:
        extra_images = extra_images.filter(project__category__slug=category_slug)

    items = []
    for project in projects:
        if project.cover_image:
            items.append({
                "image": project.cover_image,
                "caption": project.title,
                "category_slug": project.category.slug if project.category else "",
                "category_name": project.category.name if project.category else "",
                "project": project,
            })
    for image in extra_images:
        items.append({
            "image": image.image,
            "caption": image.caption or image.project.title,
            "category_slug": image.project.category.slug if image.project.category else "",
            "category_name": image.project.category.name if image.project.category else "",
            "project": image.project,
        })

    return render(request, "projects/gallery.html", {
        "items": items,
        "categories": categories,
        "current_category": category_slug,
    })


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related("category", "client").prefetch_related("services", "images"),
        slug=slug,
        published=True,
    )
    next_project = Project.objects.filter(published=True).exclude(pk=project.pk).first()
    return render(request, "projects/project_detail.html", {
        "project": project,
        "next_project": next_project,
    })
