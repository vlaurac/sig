from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ArchivoView # Cambia esta línea para importar ArchivoView en lugar de Archivo

class DocumentForm(forms.ModelForm):
    class Meta:
        model = ArchivoView  
        fields = ['documento']

class SignupForm(UserCreationForm):
    class Meta:
        model = User    
        fields = ['username', 'password1', 'password2']
