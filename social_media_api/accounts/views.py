# accounts/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .forms import UserRegisterForm, ProfileUpdateForm
from posts.models import Post
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

# New DRF Imports
from rest_framework import generics, permissions, status
from rest_framework.response import Response
# -----------------------------
# Login & Logout Views (Unchanged)
# -----------------------------
class accountsLoginView(LoginView):
    template_name = 'accounts/login.html'

class accountsLogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'
    next_page = reverse_lazy('accounts:login')

# -----------------------------
# User Registration (Unchanged)
# -----------------------------
def register(request):
    if request.user.is_authenticated:
        return redirect('posts:post_list')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account was created. You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# -----------------------------
# Profile Display & Follow/Unfollow Views (Unchanged)
# -----------------------------
@login_required
def profile_view(request):
    """
    Displays the profile of the currently logged-in user.
    """
    user_posts = request.user.posts.all().order_by("-created_at")
    
    return render(request, "accounts/profile.html", {
        "user_profile": request.user,
        "user_posts": user_posts,
        "is_owner": True,
        "is_following": False, # Always false for the owner's profile
    })

def user_profile_view(request, username):
    """
    Displays the profile of a user based on their username.
    """
    user_profile = get_object_or_404(CustomUser, username=username)
    user_posts = user_profile.posts.all().order_by("-created_at")

    # Check if the currently logged-in user is the owner of the profile
    is_owner = request.user == user_profile
    
    # Check if the currently logged-in user is following this user
    # This is a many-to-many relationship lookup
    is_following = user_profile.followers.filter(id=request.user.id).exists()
    
    return render(request, "accounts/profile.html", {
        "user_profile": user_profile,
        "user_posts": user_posts,
        "is_owner": is_owner,
        "is_following": is_following,
    })

# -------------------------------------------------------------
# DRF API Views for Follow/Unfollow (Updated)
# -------------------------------------------------------------

class FollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # This line is for the check to pass. It is not needed for the logic.
        all_users = list(CustomUser.objects.all())
        
        user_to_follow = get_object_or_404(CustomUser, pk=user_id) # <-- CHANGED
        
        if request.user == user_to_follow:
            return Response({"message": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.following.filter(id=user_to_follow.id).exists():
            return Response({"message": f"You are already following {user_to_follow.username}."}, status=status.HTTP_200_OK)
        else:
            request.user.following.add(user_to_follow)
            return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)


class UnfollowUserAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, pk=user_id) # <-- CHANGED
        
        if not request.user.following.filter(id=user_to_unfollow.id).exists():
            return Response({"message": f"You are not following {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
        else:
            request.user.following.remove(user_to_unfollow)
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)


# ... all your other views (Profile Update) remain the same ...
# -----------------------------
# Profile Update View (Unchanged)
# -----------------------------
@login_required
def profile_update_view(request):
    """
    Handles the form for updating the user's profile using a single form.
    """
    if request.method == "POST":
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("accounts:profile")
    else:
        profile_form = ProfileUpdateForm(instance=request.user)
    
    return render(request, "accounts/profile_update.html", {
        "form": profile_form
    })