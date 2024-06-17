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

from core.views import importar,descargar,exito,añadir_carrera,descargar_activos,añadir_responsable,añadir_ubicacion,error,error_archivo,borrar_masivo
from core.views import index,IngresoUsuario,eliminar_elemento,logout_view,lista,añadir,exportar_excel,filtrar_datos,modificar_activo,error_Etiqueta,error_numero_serie,borrar_activos


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
    path("añadir_responsable/",añadir_responsable,name="añadir_responsable"),
    path("añadir_carrera/",añadir_carrera,name="añadir_carrera"),
    path("añadir_ubicacion/",añadir_ubicacion,name="añadir_ubicacion"),
    path("error/",error,name="error"),
    path("error_etiqueta/",error_Etiqueta,name="error"),
    path("error_numero_serie/",error_numero_serie,name="error"),
    path("error_archivo/",error_archivo,name="error_archivo"),
    path("descargar_activos/",descargar_activos,name="descargar_activos"),
    path('exportar-excel/', exportar_excel, name='exportar_excel'),
    path('eliminar/<int:elemento_id>/', eliminar_elemento, name='eliminar_elemento'),
    path('ruta-de-modificacion',modificar_activo, name='modificar_activo'),
    path('modificar-activo/<int:item_id>/',modificar_activo, name='modificar_activo'),
    path('filtrar_datos/',filtrar_datos, name='filtrar_datos'),
    path('borrar/', borrar_activos, name='borrar_activos'),
    path('borrar_masivo/', borrar_masivo, name='borrar_masivo'),
    path('admin/', admin.site.urls),]
