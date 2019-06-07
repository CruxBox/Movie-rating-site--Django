from django.db import models
from datetime import date
from movies import models as mod
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,username,email, password=None,is_active=True,is_staff=False,is_admin=False):
        if not username:
            raise ValueError(' you need a username.')
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self,username,email, password):
        user = self.create_user(
            username = username,
            email = email,
            password=password,is_staff = True
        )
        return user

    def create_superuser(self,username,email, password):
        user = self.create_user(
            username = username,
            email = email,
            password=password,is_staff = True,
        is_admin = True
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser,PermissionsMixin):
    USERNAME_FIELD = 'username'
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False) 
    REQUIRED_FIELDS = []
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    username = models.CharField(max_length=50,null=True,unique=True)
    email= models.EmailField(max_length=254,null=True)
    phone_no = models.CharField(max_length=13,null=True)
    birth_date = models.DateField(null=True,blank = True)
    objects = UserManager()

    def calc_age(self):
        self.age = date.today().year - self.birth_date.year - ((self.birth_date.day,self.birth_date.month)>(date.today().day,date.today().month))
    def __str__(self):
        if self.first_name==None or self.last_name == None:
            return "Admin"
        return self.first_name + ' ' +  self.last_name
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active


class Public_user(models.Model):
    new_user = models.OneToOneField('Person', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.new_user.username
    def highest_rated_movie(self):
        return mod.Movie_rating.objects.filter(user = self).aggregate(models.Max('rating'))[0]
    def lowest_rated_movie(self):
        return mod.Movie_rating.objects.filter(user = self).aggregate(models.Min('rating'))[0]
    def avg_rating(self):
        return mod.Movie_rating.objects.filter(user = self).aggregate(models.Avg('rating'))[0]



class Actor(models.Model):
    actor = models.OneToOneField('Person',on_delete = models.CASCADE)
    movies = models.ManyToManyField('movies.Movie',related_name = "actor")
 
    def __str__(self):
        if self.actor.first_name==None:
            return 'random_user'
        return self.actor.first_name + ' ' + self.actor.last_name

    def acting_since(self):
        return self.movies.order_by('release_date').first()
    
    def best_movie(self):
        return self.movies.Movie_rating_set.order_by('rating').first()
        
    def worst_movie(self):
        return self.movies.Movie_rating_set.order_by('-rating').first()
        

class Director(models.Model): 
    director = models.OneToOneField('Person', on_delete=models.CASCADE)
    movies = models.ManyToManyField('movies.Movie',related_name = "director")
    def __str__(self):
        return self.director.first_name + ' ' + self.director.last_name
    def directing_since(self):
        return self.Movies.order_by('release_date').first()
    
    def best_movie(self):
        return self.movies.Movie_rating_set.order_by('rating').first()
        
    def worst_movie(self):
        return self.movies.Movie_rating_set.order_by('-rating').first()
        
    
  



