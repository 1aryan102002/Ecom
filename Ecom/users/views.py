
import re

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import createuserForm, LoginForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile as UserProfile

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
    # The link in the email is /users/email-verification/<uidb64>/<token>/.
    # uidb64 is the user's pk encoded in base64; the token proves the link was
    # made by us for this user and is still valid (it stops working once
    # is_active changes, so a link can only be used once).
    try:
        # Decoding is inside the try: a tampered uidb64 raises ValueError.
        unique_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=unique_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email_verification_success')
    return redirect('email_verification_failed')


def email_verification_sent(request):
    return render(request, 'users/email_verification_sent.html')

def email_verification_success(request):
    return render(request, 'users/email_verification_success.html')

def email_verification_failed(request):
    return render(request, 'users/email_verification_failed.html')

def login(request):
    # Already logged in - nothing to do here.
    if request.user.is_authenticated:
        return redirect('hero_home')

    if request.method == 'POST':
        # AuthenticationForm.is_valid() calls authenticate() itself and rejects
        # wrong passwords and inactive (unverified) users with its own error.
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('hero_home')
    else:
        form = LoginForm(request)
    return render(request, 'users/login.html', {'form': form})


def User_logout(request):
    # Logout only on POST (the navbar sends a small form with a CSRF token), so
    # another site can't log users out with a plain link or <img> tag.
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('hero_home')
    return render(request, 'users/logout.html')

@login_required  # anonymous users go to LOGIN_URL ('login')
def Profile(request):
    # Users made before Profile existed (e.g. createsuperuser) have no row yet
    profile = UserProfile.objects.filter(user=request.user).first()
    return render(request, 'users/profile_page.html', {'profile': profile})





