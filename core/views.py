from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from core.models import inventario

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
        # Obtener todos los objetos Inventario de la base de datos
        listado = inventario.objects.all()
        # Pasar los objetos Inventario y el usuario actual al contexto de la plantilla
        context = {
            'listado': listado,
            'user': request.user,
        }
        # Renderizar la plantilla listar.html con el contexto proporcionado
        return render(request, 'core/listar.html', context)
    else:
        # Si el usuario no está autenticado, redirigir a la página de inicio de sesión
        return redirect('/login/')

    
def añadir(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Procesar los datos del formulario POST
            etiqueta = request.POST.get('etiqueta')
            numero_serie = request.POST.get('numero_serie')
            descripcion = request.POST.get('descripcion_equipamiento')
            responsable = request.POST.get('responsable')
            carrera = request.POST.get('carrera')
            ubicacion = request.POST.get('ubicacion')
            observacion = request.POST.get('observacion')
            digitador = request.POST.get('digitador')
            
            # Guardar los datos en la base de datos
            nuevo_objeto = inventario(
            Etiqueta = etiqueta,
            Numero_Serie = numero_serie,
            Descripcion_Equipamiento = descripcion,
            Responsable = responsable,
            Carrera = carrera,
            Ubicacion = ubicacion,
            Observacion=observacion,
            Digitador=digitador,
)
            nuevo_objeto.save()

            # Redirigir a una página de éxito o donde desees después de guardar los datos
            return redirect('/exito/')  # Reemplaza '/exito/' con la URL de tu página de éxito
        else:
            return render(request, "core/añadir.html", {'user': request.user})
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