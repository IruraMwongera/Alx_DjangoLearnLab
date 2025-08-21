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

# -----------------------------
# Login & Logout Views
# -----------------------------
class accountsLoginView(LoginView):
    template_name = 'accounts/login.html'

class accountsLogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'
    next_page = reverse_lazy('accounts:login')

# -----------------------------
# User Registration
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
# Profile Display & Follow/Unfollow Views
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


@login_required
@require_POST
def follow_user(request, username):
    """
    Allows a logged-in user to follow another user via a POST request.
    """
    user_to_follow = get_object_or_404(CustomUser, username=username)

    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself.")
    elif request.user.following.filter(id=user_to_follow.id).exists():
        messages.info(request, f"You are already following {user_to_follow.username}.")
    else:
        request.user.following.add(user_to_follow)
        messages.success(request, f"You are now following {user_to_follow.username}.")
    
    # Redirect back to the user's profile page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('posts:post_list')))


@login_required
@require_POST
def unfollow_user(request, username):
    """
    Allows a logged-in user to unfollow another user via a POST request.
    """
    user_to_unfollow = get_object_or_404(CustomUser, username=username)

    if request.user.following.filter(id=user_to_unfollow.id).exists():
        request.user.following.remove(user_to_unfollow)
        messages.success(request, f"You have unfollowed {user_to_unfollow.username}.")
    else:
        messages.info(request, f"You are not following {user_to_unfollow.username}.")
    
    # Redirect back to the user's profile page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('posts:post_list')))


# -----------------------------
# Profile Update View
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