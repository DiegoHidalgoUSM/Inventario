"""
URL configuration for Inventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from core.views import index,IngresoUsuario,logout_view,lista,añadir,importar,descargar,exito

urlpatterns = [
    path("",index),
    path("home/",index),
    path("login/",IngresoUsuario),
    path("logout/",logout_view,name="logout"),
    path("lista/",lista,name="lista"),
    path("añadir/",añadir,name="añadir"),
    path("importar/",importar,name="importar"),
    path("descargar/",descargar,name="descargar"),
    path("exito/",exito,name="exito"),
    path('admin/', admin.site.urls),
]
