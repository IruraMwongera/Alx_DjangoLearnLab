from django.shortcuts import render

def home(request):
    return render(request, "base.html")  # or create a dedicated home.html extending base.html
