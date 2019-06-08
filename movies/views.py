from django.shortcuts import render
from .models import Movie,Movie_rating
from users import models
from django.http import HttpResponseRedirect
from django.urls import reverse
def display(request):
    context = {
        'movies' : Movie.objects.all()
    }
    return render(request,'movies/home.html',context)
def submit_rating(request,movie_id):
    rating_movie = Movie.objects.get(id = movie_id)
    object = Movie_rating.objects.get(movie = rating_movie, user = request.user.public_user)
    if object:
        object.rating = request.POST.get('rating')
        object.save()
    else:
        Movie_rating.objects.create(movie=rating_movie,user = request.user.public_user,rating = request.POST.get("rating"))
    
    return HttpResponseRedirect(reverse('movie-display',))
    

