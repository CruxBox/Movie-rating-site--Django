from django.shortcuts import render
from .models import Movie
from users import models

# Create your views here.


def display(request):
    context = {
        'movies' : Movie.objects.all()
    }
    return render(request,'movies/home.html',context)
