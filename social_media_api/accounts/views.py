# accounts/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()


# ------------------------------
# Register View
# ------------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)  # DRF Token

        # Handle HTML form submission
        if request.content_type == "application/x-www-form-urlencoded":
            return redirect(reverse_lazy("login"))

        # JSON/API response
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })


# ------------------------------
# Login View
# ------------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)

        # Handle HTML form submission
        if request.content_type == "application/x-www-form-urlencoded":
            return redirect(reverse_lazy("profile"))

        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })


# ------------------------------
# Profile View
# ------------------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
