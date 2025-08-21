from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# This is the crucial line for namespacing
app_name = 'accounts'

urlpatterns = [
    path('login/', views.accountsLoginView.as_view(), name='login'),
    path('logout/', views.accountsLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
]
    