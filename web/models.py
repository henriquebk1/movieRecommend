from django.db import models
from django.contrib.auth.models import Permission, User

# Create your models here.

class Movie(models.Model):
	title   	 = models.TextField()
	genres  		= models.TextField()
	poster_path  = models.TextField() 
	production_companies = models.TextField() 
	overview	= models.TextField()
	vote_average = models.FloatField()
	vote_count = models.IntegerField()

	def __str__(self):
		return self.title

class MovieRating(models.Model):
	user   	= models.ForeignKey(User,on_delete=models.CASCADE) 
	movie 	= models.ForeignKey(Movie,on_delete=models.CASCADE)
	rating 	= models.IntegerField()