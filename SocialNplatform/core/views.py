from __future__ import annotations
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SignUpForm, ProfileForm, PostForm, CommentForm
from .models import Profile, Post, Comment, Like, Follow


def ensure_profile_exists(user: User) -> None:
    Profile.objects.get_or_create(user=user)


def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data.get("email", ""),
                password=form.cleaned_data["password"],
            )
            ensure_profile_exists(user)
            login(request, user)
            messages.success(request, "Welcome!")
            return redirect("feed")
    else:
        form = SignUpForm()
    return render(request, "auth/signup.html", {"form": form})


@login_required
def feed_view(request: HttpRequest) -> HttpResponse:
    ensure_profile_exists(request.user)
    posts = (
        Post.objects.select_related("author")
        .prefetch_related("comments", "likes")
        .order_by("-created_at")[:100]
    )
    return render(request, "feed.html", {"posts": posts, "post_form": PostForm(), "comment_form": CommentForm()})


@login_required
def post_create_view(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        raise Http404()
    form = PostForm(request.POST)
    if form.is_valid():
        Post.objects.create(author=request.user, content=form.cleaned_data["content"]) 
    return redirect("feed")


@login_required
@require_POST
def comment_create_view(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        Comment.objects.create(post=post, author=request.user, content=form.cleaned_data["content"]) 
    return redirect("feed")


@login_required
@require_POST
def toggle_like_view(request: HttpRequest, post_id: int) -> JsonResponse:
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    liked = True
    if not created:
        like.delete()
        liked = False
    return JsonResponse({"liked": liked, "likes_count": post.likes.count()})


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    ensure_profile_exists(user)
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    posts = Post.objects.filter(author=user).order_by("-created_at")
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    return render(
        request,
        "profile.html",
        {
            "profile_user": user,
            "posts": posts,
            "is_following": is_following,
            "followers_count": followers_count,
            "following_count": following_count,
            "profile_form": ProfileForm(instance=user.profile),
        },
    )


@login_required
@require_POST
def toggle_follow_view(request: HttpRequest, username: str) -> JsonResponse:
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return JsonResponse({"error": "cannot_follow_self"}, status=400)
    relation, created = Follow.objects.get_or_create(follower=request.user, following=target)
    following = True
    if not created:
        relation.delete()
        following = False
    followers_count = Follow.objects.filter(following=target).count()
    return JsonResponse({"following": following, "followers_count": followers_count})


@login_required
def profile_edit_view(request: HttpRequest) -> HttpResponse:
    ensure_profile_exists(request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "profile_edit.html", {"form": form})

