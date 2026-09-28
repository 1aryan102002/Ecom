from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile

class createuserForm(UserCreationForm):
    # Not on User - saved to Profile in save()
    phone_number = forms.CharField(max_length=15, required=False)
    recovery_email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # password1/password2 are added by UserCreationForm

    def __init__(self, *args, **kwargs):
        super(createuserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'  # Add Bootstrap class to all fields
            field.widget.attrs['placeholder'] = field.label  # Set placeholder to the field's label
            field.widget.attrs.update({ 'class': "w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500" })  # Add Tailwind CSS classes
    
    def save(self, commit=True):
        user = super().save(commit)  # UserCreationForm hashes the password here
        if commit:
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                recovery_email=self.cleaned_data['recovery_email'],
            )
        return user

class LoginForm(AuthenticationForm):
    # Same Tailwind look as the register form.
    input_classes = "w-full p-2 rounded-md bg-white text-[#0f1111] border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#febd69]"

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': 'Invalid username or password.',
        'inactive': 'Please verify your email before logging in.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': self.input_classes, 'placeholder': 'Username', 'id': 'login-username'})
        self.fields['password'].widget.attrs.update({'class': self.input_classes, 'placeholder': 'Password', 'id': 'login-password'})

    def clean(self):
        # Django's ModelBackend returns None for inactive users, so an
        # unverified user would only see "Invalid username or password".
        # If the password is right but the account is inactive, say so instead.
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = User.objects.filter(username=username).first()
            if user and not user.is_active and user.check_password(password):
                raise forms.ValidationError(self.error_messages['inactive'], code='inactive')
        return super().clean()
