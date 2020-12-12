from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.models import  User
from .models import UserProfile,FriendRequest
from django import forms

class UserCreateForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2','first_name','last_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['age']

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model=FriendRequest
        fields=['receiver']