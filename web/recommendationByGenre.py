import numpy as np
import pandas as pd
from web.models import MovieRating, Movie
from math import pow, sqrt
from django.db.models import Case, When


def MyrecommendGenre(userid):
	ratings = pd.DataFrame(list(MovieRating.objects.filter(user_id = userid).values()))
	if ratings.empty:
		return []
	ratings = ratings.sort_values(by=['rating'])
	mean = ratings['rating'].mean() if ratings.size > 0 else 0
	movie_ids = ratings[ratings['rating']>=mean]['movie_id']
	preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(movie_ids)])
	movie_list=list(Movie.objects.filter(id__in = movie_ids).order_by(preserved)[:50])

	genres = set() 
	for movie in movie_list:
		genres.add(movie.genres)

	df=pd.DataFrame(list(Movie.objects.filter(genres__in = genres).exclude(id__in = ratings['movie_id']).values()))
	C = df.vote_average.mean()
	m = df.vote_count.quantile(0.90)
	q_movies = df.copy().loc[df.vote_count >= m]
	q_movies.shape
	def weighted_rating1(x, m=m, C=C):
		v = x['vote_count']
		R = x['vote_average']
		return (v/(v+m) * R) + (m/(m+v) * C)
	
	q_movies['score'] = q_movies.apply(weighted_rating1, axis=1)
	q_movies = q_movies.sort_values('score', ascending=False)
	q_movies = q_movies.head(100)
	
	return [Movie(
			id=record['id'],
			title=record['title'],
			genres=record['genres'],
			poster_path=record['poster_path'],
			production_companies=record['production_companies'],
			overview=record['overview'],
			vote_average=record['vote_average'],
			vote_count=record['vote_count'],
	) for record in q_movies.to_dict('records')]
	







