from django.contrib import admin
from django.urls import path, include  # <-- include is required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home route pointing to login
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='home'),

    # Explicit login/logout routes
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    # Include blog app URLs
    path('', include('blog.urls')),  # <-- add this line
]
