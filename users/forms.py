from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from localflavor.in_.forms import INZipCodeField,INStateField

from .models import Location, Profile
from .widgets import CustomPictureImageFieldWidget


class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=CustomPictureImageFieldWidget)
    bio = forms.TextInput()

    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'phone_number')


class LocationForm(forms.ModelForm):

    address_1 = forms.CharField(required=True)
    zip_code = INZipCodeField(required=True)

    class Meta:
        model = Location
        fields = {'address_1', 'address_2', 'city', 'state', 'zip_code'}
        

# customuserform
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {
            'username': 'Once set, your username cannot be changed.',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()  # Check if user exists

        if user:
            if user.is_active:
                # If the user is active, prevent registration
                raise ValidationError("This email is already registered. Please try logging in.")
            else:
                user.delete()
        else:
            return email

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
# otp
class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter the 6-digit OTP")