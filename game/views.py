from hashlib import sha1
import base64
import hashlib
import hmac
import logging
import os
import time
import urllib
import urllib.parse

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .forms import LoginForm, UploadCarsForm, ScoreForm

from .models import GameUser


@login_required()
@permission_required('game.view_game')
def index(request):
	context_dict = {}
	instance = GameUser.objects.get(user__username=request.user.username)
	if request.method == 'POST':
		form = UploadCarsForm(request.POST, request.FILES, instance=instance)

		if form.is_valid():
			instance.car_1 = form.cleaned_data['car_1']
			instance.car_2 = form.cleaned_data['car_2']
			instance.car_3 = form.cleaned_data['car_3']
			instance.car_4 = form.cleaned_data['car_4']
			instance.car_5 = form.cleaned_data['car_5']
			instance.save()
			return redirect('game:index')
	else:
		form = UploadCarsForm(initial=model_to_dict(instance))

	context_dict['form'] = form
	context_dict['game_user'] = instance
	return render(request, 'game/index.html', context_dict)


@login_required()
@permission_required('game.view_game')
def level_1(request):
	context_dict = {}
	game_user = GameUser.objects.get(user=request.user)
	context_dict['game_user'] = game_user


	if game_user.car_1:
		context_dict['svg_car'] = game_user.car_1
	else:
		context_dict['svg_car'] = ''

	if request.method == 'POST':
		form = ScoreForm(request.POST)

		if form.is_valid():
			game_user.score_level_1 = form.cleaned_data['score']
			game_user.save()
			return redirect('game:index')
	else:
		form = ScoreForm()
	
	context_dict['send_score_form'] = form

	context_dict['level'] = 'svg/terrain2.svg'
	return render(request, 'game/race.html', context_dict)


@login_required()
@permission_required('game.view_game')
def level_2(request):
	context_dict = {}
	game_user = GameUser.objects.get(user=request.user)
	context_dict['game_user'] = game_user
	
	if game_user.car_2:
		context_dict['svg_car'] = game_user.car_2
	else:
		context_dict['svg_car'] = ''

	if request.method == 'POST':
		form = ScoreForm(request.POST)

		if form.is_valid():
			game_user.score_level_2 = form.cleaned_data['score']
			game_user.save()
			return redirect('game:index')
	else:
		form = ScoreForm()
	
	context_dict['send_score_form'] = form
	
	context_dict['level'] = 'svg/terrain2.svg'
	return render(request, 'game/race.html', context_dict)


@login_required()
@permission_required('game.view_game')
def level_3(request):
	context_dict = {}
	game_user = GameUser.objects.get(user=request.user)
	context_dict['game_user'] = game_user

	if game_user.car_3:
		context_dict['svg_car'] = game_user.car_3
	else:
		context_dict['svg_car'] = ''

	if request.method == 'POST':
		form = ScoreForm(request.POST)

		if form.is_valid():
			game_user.score_level_3 = form.cleaned_data['score']
			game_user.save()
			return redirect('game:index')
	else:
		form = ScoreForm()
	
	context_dict['send_score_form'] = form

	context_dict['level'] = 'svg/terrain2.svg'
	return render(request, 'game/race.html', context_dict)


@login_required()
@permission_required('game.view_game')
def level_4(request):
	context_dict = {}
	game_user = GameUser.objects.get(user=request.user)
	context_dict['game_user'] = game_user
	
	if game_user.car_4:
		context_dict['svg_car'] = game_user.car_4
	else:
		context_dict['svg_car'] = ''

	if request.method == 'POST':
		form = ScoreForm(request.POST)

		if form.is_valid():
			game_user.score_level_4 = form.cleaned_data['score']
			game_user.save()
			return redirect('game:index')
	else:
		form = ScoreForm()
	
	context_dict['send_score_form'] = form

	context_dict['level'] = 'svg/terrain2.svg'
	return render(request, 'game/race.html', context_dict)


@login_required()
@permission_required('game.view_game')
def level_5(request):
	context_dict = {}
	game_user = GameUser.objects.get(user=request.user)
	context_dict['game_user'] = game_user

	if game_user.car_2:
		context_dict['svg_car'] = game_user.car_5
	else:
		context_dict['svg_car'] = ''

	if request.method == 'POST':
		form = ScoreForm(request.POST)

		if form.is_valid():
			game_user.score_level_5 = form.cleaned_data['score']
			game_user.save()
			return redirect('game:index')
	else:
		form = ScoreForm()
	
	context_dict['send_score_form'] = form

	context_dict['level'] = 'svg/terrain2.svg'
	return render(request, 'game/race.html', context_dict)


def game_auth(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return redirect('game:index')
			else:
				return HttpResponse('Your account is disabled')
		else:
			print("Invalid login details: {0}, {1}.".format(username, password))
			return HttpResponse("Invalid login details supplied")

	else:
		return render(request, 'game/login.html', {})


@csrf_protect
def game_login(request):
	form = LoginForm()
	context_dict = {'form': form}
	return render(request, 'game/login.html', context_dict)


@login_required()
def game_logout(request):
	logout(request)
	return redirect('game:login')