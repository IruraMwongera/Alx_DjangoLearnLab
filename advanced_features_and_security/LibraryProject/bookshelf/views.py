from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def add_book(request):
    return HttpResponse("This is the Add Book page.")

