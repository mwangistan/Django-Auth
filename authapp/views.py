# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from authapp.forms import EmailConfimationForm
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse

class CustomLoginView(LoginView):
	'''
		Class to redirect user to provide email address if it doesn't exist
	'''

	form_class = AuthenticationForm
	template_name = 'registration/login.html'

	def form_valid(self, form):
		user = User.objects.get(username=self.request.user.username)
		if user.email == '':
			return redirect('/email_confirmation')
		else:
			auth_login(self.request, form.get_user())
			return redirect(self.get_success_url())

class EmailConfirmation(View):
	form_class = EmailConfimationForm
	template_name = 'emailconfirm.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			print('valid')
			return HttpResponse('An email confirmation link has been sent to your email address')
		return render(request, self.template_name, {'form': form})