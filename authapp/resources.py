from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.shortcuts import redirect

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    '''
    Token generator for email link activation. Inherits PasswordResetTokenGenerator
    '''
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) +  six.text_type(user.is_active)

account_activation_token = AccountActivationTokenGenerator()


def activate(request, uidb64, token, email):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email = email
        user.save()
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')