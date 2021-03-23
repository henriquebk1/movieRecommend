import numpy as np
import pandas as pd
from web.models import MovieRating
from math import pow, sqrt


def Myrecommend(userid):
	ratings = pd.DataFrame(list(MovieRating.objects.all().values()))
	user_ids = ratings.user_id.unique().tolist()
	total = {}
	similariy_sum = {}

	def get_rating_(userid,movieid):
		return (ratings.loc[(ratings.user_id==userid) & (ratings.movie_id == movieid),'rating'].iloc[0])

	# Function to get the list of all movie ids the specified user has rated.
	def get_movieids_(userid):
		return (ratings.loc[(ratings.user_id==userid),'movie_id'].tolist())
	
	def pearson_correlation_score(user1,user2):
		'''
		user1 & user2 : user ids of two users between which similarity score is to be calculated.
		'''
		both_watch_count = []
		for element in ratings.loc[ratings.user_id==user1,'movie_id'].tolist():
			if element in ratings.loc[ratings.user_id==user2,'movie_id'].tolist():
				both_watch_count.append(element)
		if len(both_watch_count) == 0:
			return 0
		rating_sum_1 = sum([get_rating_(user1,element) for element in both_watch_count])
		rating_sum_2 = sum([get_rating_(user2,element) for element in both_watch_count])
		rating_squared_sum_1 = sum([pow(get_rating_(user1,element),2) for element in both_watch_count])
		rating_squared_sum_2 = sum([pow(get_rating_(user2,element),2) for element in both_watch_count])
		product_sum_rating = sum([get_rating_(user1,element) * get_rating_(user2,element) for element in both_watch_count])
    
		numerator = product_sum_rating - ((rating_sum_1 * rating_sum_2) / len(both_watch_count))
		denominator = sqrt((rating_squared_sum_1 - pow(rating_sum_1,2) / len(both_watch_count)) * (rating_squared_sum_2 - pow(rating_sum_2,2) / len(both_watch_count)))
		if denominator == 0:
			return 0
		return numerator/denominator

	# Iteratin over subset of user ids.
	for user in user_ids[:1000]:
		if user == userid:
			continue
		
		# Getting similarity score between the users.
		score = pearson_correlation_score(userid,user)
		
		# not considering users having zero or less similarity score.
		if score <= 0:
			continue
		
		# Getting weighted similarity score and sum of similarities between both the users.
		for movieid in get_movieids_(user):
			# Only considering not watched/rated movies
			if movieid not in get_movieids_(userid) or get_rating_(userid,movieid) == 0:
				total[movieid] = 0
				total[movieid] += get_rating_(user,movieid) * score
				similariy_sum[movieid] = 0
				similariy_sum[movieid] += score
	
	# Normalizing ratings
	ranking = [(tot/similariy_sum[movieid],movieid) for movieid,tot in total.items()]
	ranking.sort()
	ranking.reverse()

	return [ x[1] for x in ranking]
	







