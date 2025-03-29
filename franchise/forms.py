from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
    
    username = forms.CharField(max_length = 100,widget = forms.TextInput(attrs={'placeholder':'Enter Your FullName'}))
    email = forms.EmailField(widget = forms.EmailInput(attrs={'placeholder':'Enter Your Email'}))
