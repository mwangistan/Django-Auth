# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from authapp.forms import EmailConfimationForm
from authapp.resources import account_activation_token

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
			current_site = get_current_site(request)
			message = render_to_string('active_email.html',{
            	'user':self.request.user, 
            	'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(self.request.user.pk)),
                'token': account_activation_token.make_token(self.request.user),
                })

			mail_subject = 'Confirm your email address'
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			return HttpResponse('An email confirmation link has been sent to your email address')
		return render(request, self.template_name, {'form': form})