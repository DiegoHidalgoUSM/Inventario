from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from core.models import Inventario,Responsables,Carreras

def IngresoUsuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Nombre de usuario o contraseña no válidos')
            return redirect('/login/') 
    else:
        return render(request,"core/login.html")

def index(request):
    if request.user.is_authenticated:
        return render(request, "core/home.html", {'user': request.user})
    else:
        return redirect('/login/')

def logout_view(request):
    auth_logout(request)
    return redirect('/login/')

def lista(request):
    if request.user.is_authenticated:
        listado = Inventario.objects.all()
        context = {
            'listado': listado,
            'user': request.user,
        }
        return render(request, 'core/listar.html', context)
    else:
        return redirect('/login/')

    
from django.shortcuts import render, redirect
from .models import inventario, Responsables

def añadir(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            etiqueta = request.POST.get('etiqueta')
            numero_serie = request.POST.get('numero_serie')
            descripcion = request.POST.get('descripcion_equipamiento')
            responsable = request.POST.get('responsable')
            carrera= request.POST.get('carrera')
            ubicacion = request.POST.get('ubicacion')
            observacion = request.POST.get('observacion')
            responsable_caja = request.POST.get('responsable_checkbox')
            carrera_caja = request.POST.get('carrera_checkbox')
            if responsable_caja:
                nuevo_responsable = Responsables(nombre=responsable)
                nuevo_responsable.save()
            
            if carrera_caja:
                nueva_Carrera=Carreras(nombre=carrera)
                nueva_Carrera.save()

            carrera = carreras.objects.get(id=carrera)

            nuevo_objeto = Inventario(
                Etiqueta=etiqueta,
                Numero_Serie=numero_serie,
                Descripcion_Equipamiento=descripcion,
                Responsable=responsable,
                Carrera=carrera,
                Ubicacion=ubicacion,
                Observacion=observacion,
                Digitador=request.user,
            )
            nuevo_objeto.save()

            return redirect('/exito/')
        else:
            responsables = Responsables.objects.all()
            carreras = carreras.objects.all()
            context = {
                'responsables': responsables,
                'carreras': carreras,
                'user': request.user,
            }
            return render(request, "core/añadir.html", context)
    else:
        return redirect('/login/')

    
def importar(request):
    if request.user.is_authenticated:
        return render(request,"core/importar.html", {'user': request.user})
    else:
        return redirect('/login/')
    
def descargar(request):
    if request.user.is_authenticated:
        return render(request,"core/descargar.html", {'user': request.user})
    else:
        return redirect('/login/')
    
def exito(request):
    if request.user.is_authenticated:
        return render(request,"core/exito.html", {'user': request.user})
    else:
        return redirect('/login/')