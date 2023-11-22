# sig/forms.py
from django import forms
from django.contrib.auth.models import User  # Agrega esta línea
from django.contrib.auth.forms import UserCreationForm
from .models import ArchivoView

class DocumentForm(forms.ModelForm):
    class Meta:
        model = ArchivoView
        fields = ['documento']

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
