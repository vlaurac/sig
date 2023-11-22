from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.staticfiles.views import serve as serve_static
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .forms import DocumentForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ArchivoView

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Las contraseñas no coinciden.",
    }

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Puedes personalizar los mensajes de error aquí si es necesario
        # self.error_messages['some_error'] = "Some custom error message"

def login_view(request):
    error = None

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('sigS')
        else:
            error = 'Invalid username or password'
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'error': error})



class Archivo(models.Model):
    documento = models.FileField(upload_to='archivos/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.documento.name

def calidad(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_archivo = form.save()
            return redirect('calidad')
    else:
        form = DocumentForm()

    archivos = ArchivoView.objects.all() 
    return render(request, 'sitem/calidad.html', {'form': form, 'archivos': archivos})

def serve_documento(request, archivo_path):
    return serve_static(request, path=archivo_path, insecure=True)

def editar_archivo(request, archivo_id):
    archivo = get_object_or_404(Archivo, id=archivo_id)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=archivo)
        if form.is_valid():
            form.save()
            return redirect('calidad')
    else:
        form = DocumentForm(instance=archivo)

    return render(request, 'sitem/editar_archivo.html', {'form': form, 'archivo': archivo})
def eliminar_archivo(request, archivo_id):
    archivo = get_object_or_404(Archivo, id=archivo_id)

    if request.method == 'POST':
        archivo.delete()
        return redirect('calidad')

    return render(request, 'sitem/eliminar_archivo.html', {'archivo': archivo})

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('sigS') 
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def generar_reporte_pdf(request):
    archivos = Archivo.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

    # Acceder al usuario actual
    user = request.user if request.user.is_authenticated else None
    user_name = user.username if user else 'Anónimo'

    pdf = SimpleDocTemplate(response, pagesize=letter)
    data = []

    # Agregar información del usuario
    data.append(['Usuario que modificó los archivos o agrego :', user_name])
    data.append(['Documento', 'Fecha de Creación'])

    for archivo in archivos:
        data.append([archivo.documento.name, archivo.fecha_creacion])

    tabla = Table(data)
    estilo = TableStyle([
       ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
       ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
       ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
       ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
       ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
       ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    tabla.setStyle(estilo)

    elementos = [tabla]
    pdf.build(elementos)

    return response

def sst(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_archivo = form.save()
            return redirect('sst')
    else:
        form = DocumentForm()

    archivos = ArchivoView.objects.all() 
    return render(request, 'sitem/sst.html', {'form': form, 'archivos': archivos})

def medioambiente(request):
    return render(request, 'sitem/medioambiente.html')

def sigS(request):
    return render(request, 'sigS.html')
