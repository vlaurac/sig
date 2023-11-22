"""
URL configuration for Sistemas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.static import serve
from sig import views
from django.conf.urls.static import static
from sig.views import generar_reporte_pdf, login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', login_view, name='login'),
    path('sigS/', views.sigS, name='sigS'),
    path('calidad/', views.calidad, name='calidad'),
    path('sst/', views.sst, name='sst'),
    path('medioambiente/', views.medioambiente, name='medioambiente'),
    path('documentos/<path:archivo_path>/', views.serve_documento, name='serve_documento'),
    path('editar_archivo/<int:archivo_id>/', views.editar_archivo, name='editar_archivo'),
    path('eliminar_archivo/<int:archivo_id>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('generar_reporte_pdf/', generar_reporte_pdf, name='generar_reporte_pdf'),
]

# Asegúrate de que la línea anterior esté alineada con el 'urlpatterns'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
