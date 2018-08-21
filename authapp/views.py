# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from two_factor.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from authapp.forms import EmailConfimationForm
from authapp.resources import account_activation_token

class CustomLoginView(LoginView):
	'''
	Custom login view that inherits 2factor auth login view to check 
	if email address is provided before login
	'''
	def post(self, *args, **kwargs):
		try:
			user = User.objects.get(username=self.request.POST.get('auth-username'))
			if user.email == '':
				self.request.session['username'] = self.request.POST.get('auth-username')
				return redirect('/email_confirmation')
		except:
			pass
		if 'challenge_device' in self.request.POST:
			return self.render_goto_step('token')

		return super(LoginView, self).post(*args, **kwargs)

class EmailConfirmation(View):
	'''
	View to display email confirmation form and to send email address to
	provided email
	'''
	form_class = EmailConfimationForm
	template_name = 'emailconfirm.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		user = User.objects.get(username=request.session['username'])
		if form.is_valid():
			current_site = get_current_site(request)
			message = render_to_string('active_email.html',{
            	'user':user,
            	'email': form.cleaned_data.get('email'),
            	'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                })
			del request.session['username']

			mail_subject = 'Confirm your email address'
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			return HttpResponse('An email confirmation link has been sent to your email address')
		return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

def profile_view(request):
	return render(request, 'profile.html')