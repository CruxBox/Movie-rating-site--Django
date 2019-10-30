from django.shortcuts import render
from .models import Movie,Movie_rating
from users import models
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
def display(request):
    context = {
        'movies' : Movie.objects.all()
    }
    return render(request,'movies/home.html',context)
def submit_rating(request,movie_id):
    rating_movie = Movie.objects.get(id = movie_id)
    if request.user.is_staff:
        return HttpResponse('Admins cannot rate. Login as non-admin.',content_type="text/plain")
    temp_object = Movie_rating.objects.filter(movie = rating_movie, user = request.user.public_user)
    if temp_object:
        temp_object = temp_object[0]
        temp_object.rating = request.POST.get('rating')
        temp_object.save()
    else:
        Movie_rating.objects.create(movie=rating_movie,user = request.user.public_user,rating = request.POST.get("rating"))
    
    return HttpResponseRedirect(reverse('movie-display',))
    

