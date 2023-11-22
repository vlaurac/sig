# models.py

from django.db import models
from django.utils import timezone

class ArchivoView(models.Model):
    documento = models.FileField(upload_to='archivo/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.documento.name
