from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings

from contact.models import Message
from projects.models import Project, ProjectImage
from testimonials.models import Testimonial
from blog.models import Post
from services.models import Service

from .forms import MessageForm, ProjectForm, ProjectImageForm, PostForm, ServiceForm


def staff_required(user):
    return user.is_staff

# Login view
def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:dashboard_index')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('dashboard:dashboard_index')
            else:
                messages.error(request, "You do not have staff access.")
        else:
            # Form invalid -> shows errors automatically
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            for error in form.non_field_errors():
                messages.error(request, error)

    return render(request, 'dashboard/login.html', {'form': form})

# Logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard:login')

# Dashboard
@login_required
@user_passes_test(staff_required)
def dashboard_index(request):
    context = {
        "unread_count": Message.objects.filter(is_read=False).count(),
        "project_count": Project.objects.count(),
        "latest_messages": Message.objects.order_by("-created")[:5],
        "pending_testimonials_count": Testimonial.objects.filter(approved=False).count(),
    }
    return render(request, 'dashboard/index.html', context)


@login_required
@user_passes_test(staff_required)
def messages_list(request):
    qs = Message.objects.all()
    paginator = Paginator(qs, 15)
    items = paginator.get_page(request.GET.get("page"))
    return render(request, "dashboard/messages_list.html", {"messages_page": items})


@login_required
@user_passes_test(staff_required)
def message_view(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard_messages")
    else:
        if not message.is_read:
            message.is_read = True
            message.save(update_fields=["is_read"])
        form = MessageForm(instance=message)
    return render(request, "dashboard/message_view.html", {"message": message, "form": form})


@login_required
@user_passes_test(staff_required)
def projects_list(request):
    projects = Project.objects.all().order_by("-created")
    return render(request, "dashboard/projects_list.html", {"projects": projects})


@login_required
@user_passes_test(staff_required)
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard_projects")
    else:
        form = ProjectForm()
    return render(request, "dashboard/project_form.html", {"form": form})


@login_required
@user_passes_test(staff_required)
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard_projects")
    else:
        form = ProjectForm(instance=project)
    image_form = ProjectImageForm()
    return render(request, "dashboard/project_form.html", {
        "form": form,
        "project": project,
        "image_form": image_form,
        "gallery_images": project.images.all(),
    })


@login_required
@user_passes_test(staff_required)
def project_image_add(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.project = project
            image.save()
    return redirect("dashboard:dashboard_project_edit", pk=project.pk)


@login_required
@user_passes_test(staff_required)
def project_image_delete(request, pk, image_pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        ProjectImage.objects.filter(pk=image_pk, project=project).delete()
    return redirect("dashboard:dashboard_project_edit", pk=project.pk)


@login_required
@user_passes_test(staff_required)
def testimonials_list(request):
    qs = Testimonial.objects.all().order_by("approved", "-created")
    return render(request, "dashboard/testimonials_list.html", {"testimonials": qs})


@login_required
@user_passes_test(staff_required)
def testimonial_approve(request, pk):
    if request.method == "POST":
        Testimonial.objects.filter(pk=pk).update(approved=True)
    return redirect("dashboard:dashboard_testimonials")


@login_required
@user_passes_test(staff_required)
def testimonial_decline(request, pk):
    if request.method == "POST":
        Testimonial.objects.filter(pk=pk).update(approved=False)
    return redirect("dashboard:dashboard_testimonials")


@login_required
@user_passes_test(staff_required)
def testimonial_delete(request, pk):
    if request.method == "POST":
        Testimonial.objects.filter(pk=pk).delete()
    return redirect("dashboard:dashboard_testimonials")


@login_required
@user_passes_test(staff_required)
def blog_list(request):
    posts = Post.objects.all().order_by("-created")
    return render(request, "dashboard/posts_list.html", {"posts": posts})


@login_required
@user_passes_test(staff_required)
def blog_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if not post.author_id:
                post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("dashboard:dashboard_blog")
    else:
        form = PostForm()
    return render(request, "dashboard/post_form.html", {"form": form})


@login_required
@user_passes_test(staff_required)
def blog_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard_blog")
    else:
        form = PostForm(instance=post)
    return render(request, "dashboard/post_form.html", {"form": form, "post": post})


@login_required
@user_passes_test(staff_required)
def services_list(request):
    services = Service.objects.all().order_by("order", "title")
    return render(request, "dashboard/services_list.html", {"services": services})


@login_required
@user_passes_test(staff_required)
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect("dashboard:dashboard_services")
    else:
        form = ServiceForm(instance=service)
    return render(request, "dashboard/service_form.html", {"form": form, "service": service})
