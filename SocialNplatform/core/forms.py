from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment, Profile


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar_url"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

