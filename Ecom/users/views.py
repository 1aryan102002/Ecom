
import re

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import createuserForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = createuserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False  # Set the user as inactive
            user.save()
            current_site = get_current_site(request)
            subject = "Email Verification"
            message = render_to_string('users/email_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            user.email_user(subject = subject, message = message)
            return redirect('email_verification_sent')  # Send the email to the user
            # Here you would typically send the email using Django's email sending functionality
        
            
    else:
        form = createuserForm()
          # Redirect to the same page or another page after successful registration
    return render(request, 'users/register.html', {'form': form})

def email_verification(request, uidb64, token):
    return render(request, 'users/email_verification.html')

def email_verification_sent(request):
    return render(request, 'users/email_verification_sent.html')

def email_verification_success(request):
    return render(request, 'users/email_verification_success.html')

def email_verification_failed(request):
    return render(request, 'users/email_verification_failed.html')

























