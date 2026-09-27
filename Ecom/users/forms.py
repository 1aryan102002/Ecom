from django import forms
from django.contrib.auth.forms import UserCreationForm
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
