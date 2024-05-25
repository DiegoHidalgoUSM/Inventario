from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from core.models import Inventario,Responsable,Carrera,Ubicacion

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

def añadir(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
        #metodo post
            etiqueta = request.POST.get('etiqueta')
            numero_serie = request.POST.get('numero_serie')
            descripcion = request.POST.get('descripcion_equipamiento')
            responsable_id = request.POST.get('responsable')
            carrera_id = request.POST.get('carrera')
            ubicacion_id = request.POST.get('ubicacion')
            observacion = request.POST.get('observacion')
            nuevo_responsable = request.POST.get('nuevo_responsable')
            nueva_carrera = request.POST.get('nueva_carrera')
            nueva_ubicacion = request.POST.get('nueva_ubicacion')

        #si existe el nuevo responsable
            if nuevo_responsable:
                responsable = Responsable.objects.create(nombre=nuevo_responsable)
            else:
                responsable = Responsable.objects.get(id=responsable_id)
        #si existe la nueva carrera
            if nueva_carrera:
                carrera = Carrera.objects.create(nombre=nueva_carrera)
            else:
                carrera = Carrera.objects.get(id=carrera_id)
        #si existe la nueva ubicacion
            if nueva_ubicacion:
                ubicacion = Ubicacion.objects.create(nombre=nueva_ubicacion)
            else:
                ubicacion = Ubicacion.objects.get(id=ubicacion_id)
                
        #incluir a la lista
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
            responsables = Responsable.objects.all()
            carreras = Carrera.objects.all()
            ubicaciones=Ubicacion.objects.all()
            context = {
                'responsables': responsables,
                'carreras': carreras,
                'ubicaciones': ubicaciones,
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
    
def añadir_responsable(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nombre = request.POST.get('nuevo_responsable')
            nuevo_responsable = Responsable(nombre=nombre)
            nuevo_responsable.save()
        return redirect('/añadir/') 
    else:
        return redirect('/login/')
def añadir_ubicacion(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nombre = request.POST.get('nueva_ubicacion')
            nueva_ubicacion = Ubicacion(nombre=nombre)
            nueva_ubicacion.save()
        return redirect('/añadir/')  
    else:
        return redirect('/login/')
    
def añadir_carrera(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nombre = request.POST.get('nueva_carrera')
            nueva_carrera = Carrera(nombre=nombre)
            nueva_carrera.save()
        return redirect('/añadir/')  
    else:
        return redirect('/login/')
