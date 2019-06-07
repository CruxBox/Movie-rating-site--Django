from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator,MinValueValidator


class Movie(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField()
    release_date = models.DateField(null=True,blank=True,auto_now_add=True)
    imdb_url = models.URLField(unique = True,null=True)
    pic = models.ImageField(default = 'default.jpg',upload_to = 'cover_pics')
    def get_avg_rating(self):
        return Movie_rating.objects.filter(movie__title=self.title).aggregate(models.Avg('rating'))['rating__avg']

    def __str__(self):
        return self.title
    

class Movie_rating(models.Model):
    movie = models.ForeignKey('Movie',blank=True,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey('users.Public_user',blank=True,null=True,on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)],)
    rated_on = models.DateTimeField(auto_now_add=True)

