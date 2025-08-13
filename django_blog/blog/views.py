from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# -----------------------------
# Login & Logout Views
# -----------------------------
class BlogLoginView(LoginView):
    template_name = 'registration/login.html'

class BlogLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'

# -----------------------------
# User Registration
# -----------------------------
def register(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Already logged in
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account was created. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

# -----------------------------
# Profile Management
# -----------------------------
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'blog/profile.html', context)

# -----------------------------
# Blog Posts List
# -----------------------------
@login_required
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
