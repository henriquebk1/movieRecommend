import pandas as pd
from web.models import Movie
from django.db.models import Q


def GeneralRecommend(query):
	if query:
		return Movie.objects.filter(Q(title__icontains=query) | Q(overview__icontains=query)).distinct()
	movies = Movie.objects.all()	

	df=pd.DataFrame(list(movies.values()))
	C = df.vote_average.mean()
	m = df.vote_count.quantile(0.90)
	q_movies = df.copy().loc[df.vote_count >= m]
	q_movies.shape

	def weighted_rating(x, m=m, C=C):
		v = x['vote_count']
		R = x['vote_average']
		return (v/(v+m) * R) + (m/(m+v) * C)
  
	q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
	q_movies = q_movies.sort_values('score', ascending=False)
	q_movies = q_movies.head(100)
	
	movies = [Movie(
			id=record['id'],
			title=record['title'],
			genres=record['genres'],
			poster_path=record['poster_path'],
			production_companies=record['production_companies'],
			overview=record['overview'],
			vote_average=record['vote_average'],
			vote_count=record['vote_count'],
	) for record in q_movies.to_dict('records')]
	
	return movies
	
	







