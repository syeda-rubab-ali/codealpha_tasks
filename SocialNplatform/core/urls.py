from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
 path('accounts/login/', lambda request: redirect('/login/')),
    path("feed/", views.feed_view, name="feed"),
    path("post/create/", views.post_create_view, name="post_create"),
    path("post/<int:post_id>/comment/", views.comment_create_view, name="comment_create"),
    path("post/<int:post_id>/like/", views.toggle_like_view, name="toggle_like"),

    path("u/<str:username>/", views.profile_view, name="profile"),
    path("u/<str:username>/follow/", views.toggle_follow_view, name="toggle_follow"),
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

