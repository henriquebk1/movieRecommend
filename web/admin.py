from django.contrib import admin

# Register your models here.
from .models import Movie, MovieRating

admin.site.register(Movie)
admin.site.register(MovieRating)
