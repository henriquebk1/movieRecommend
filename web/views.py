from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from django.http import Http404
from .models import Movie,MovieRating
from django.contrib import messages
from .forms import UserForm
from django.db.models import Case, When
from .recommendation import Myrecommend
from .generalRecommendation import GeneralRecommend
from .recommendationByGenre import MyrecommendGenre
import numpy as np 
import pandas as pd


# for recommendation
def recommend(request):
	if not request.user.is_authenticated:
		return redirect("login")
	if not request.user.is_active:
		raise Http404

	print("Current user id: ",request.user.id)
	pred_idxs_sorted = Myrecommend(request.user.id)
	preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
	movie_list=list(Movie.objects.filter(id__in = pred_idxs_sorted).order_by(preserved)[:50])
	return render(request,'web/recommend.html',{'movie_list':movie_list})

	# for recommendation by genre
def genres(request):
	if not request.user.is_authenticated:
		return redirect("login")
	if not request.user.is_active:
		raise Http404

	print("Current user id: ",request.user.id)
	return render(request,'web/recommend.html',{'movie_list':MyrecommendGenre(request.user.id)})


# List view
def index(request):
	movies = GeneralRecommend(request.GET.get('q'))
	return render(request,'web/list.html',{'movies':movies})


# detail view
def detail(request,movie_id):
	if not request.user.is_authenticated:
		return redirect("login")
	if not request.user.is_active:
		raise Http404
	movies = get_object_or_404(Movie,id=movie_id)
	userRating = MovieRating.objects.filter(user__id = request.user.id, movie__id = movie_id).first()
	currentRating = (0 if userRating is None else userRating.rating)
	#for rating
	if request.method == "POST":
		rate = request.POST['rating']
		ratingObject = MovieRating() if userRating is None else userRating
		ratingObject.user   = request.user
		ratingObject.movie  = movies
		ratingObject.rating = rate
		ratingObject.save()
		movie = Movie.objects.filter(id = movie_id).first()
		if  userRating is None:
			movie.vote_average = (movie.vote_average * movie.vote_count + float(rate))/(movie.vote_count + 1)
			movie.vote_count += 1
		else:
			movie.vote_average = (movie.vote_average * movie.vote_count + float(rate) - currentRating)/(movie.vote_count)
		movie.save()
		messages.success(request,"Your Rating is submited ")
		return render(request,'web/detail.html',{'movies':movies, 'rating': rate })
	return render(request,'web/detail.html',{'movies':movies, 'rating': currentRating })


# Register user
def signUp(request):
	form =UserForm(request.POST or None)
	if form.is_valid():
		user      = form.save(commit=False)
		username  =	form.cleaned_data['username']
		password  = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("index")
	context ={
		'form':form
	}
	return render(request,'web/signUp.html',context)				


# Login User
def Login(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		user     = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect("index")
			else:
				return render(request,'web/login.html',{'error_message':'Your account disable'})
		else:
			return render(request,'web/login.html',{'error_message': 'Invalid Login'})
	return render(request,'web/login.html')

#Logout user
def Logout(request):
	logout(request)
	return redirect("login")
