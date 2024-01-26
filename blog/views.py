from django.shortcuts import render
from django.http import Http404

# Create your views here.

def index(request):
    return render(request, "blog/main.html")

def posts(request):
    return

def post_detailed(request):
    return