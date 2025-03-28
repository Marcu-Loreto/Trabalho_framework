"""
URL configuration for assistencia_tecnica project.

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
#from ordens.views import index, suporte_automatico
from ordens import views
from ordens.views import index, suporte_automatico

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('suporte/', suporte_automatico, name='suporte_automatico'),
    path('computadores/importar/', views.importar_computadores, name='importar_computadores'),
    path('computadores/exportar/', views.exportar_computadores, name='exportar_computadores'),

]
