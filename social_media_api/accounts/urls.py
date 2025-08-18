from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
