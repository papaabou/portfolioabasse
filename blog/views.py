from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post


def post_list(request):
    qs = Post.objects.filter(published=True).order_by("-created")
    paginator = Paginator(qs, 6)
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, "blog/post_detail.html", {"post": post})
