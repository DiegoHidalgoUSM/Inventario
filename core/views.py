from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from core.models import Inventario,Responsable,Carrera,Ubicacion
from django.db.models import Q
from .forms import ImportForm
import pandas as pd
from django.http import HttpResponse

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
        listado = Inventario.objects.all().order_by('-id')
        filtros = request.GET.getlist('filtro')
        termino_busqueda = request.GET.get('buscar', '')

        if termino_busqueda:
            query = Q()
            for filtro in filtros:
                if filtro == 'Etiqueta':
                    query |= Q(Etiqueta__icontains=termino_busqueda)
                elif filtro == 'Numero_Serie':
                    query |= Q(Numero_Serie__icontains=termino_busqueda)
                elif filtro == 'Descripcion_Equipamiento':
                    query |= Q(Descripcion_Equipamiento__icontains=termino_busqueda)
                elif filtro == 'Responsable':
                    query |= Q(Responsable__icontains=termino_busqueda)
                elif filtro == 'Carrera':
                    query |= Q(Carrera__icontains=termino_busqueda)
                elif filtro == 'Ubicacion':
                    query |= Q(Ubicacion__icontains=termino_busqueda)
                elif filtro == 'Digitador':
                    query |= Q(Digitador__icontains=termino_busqueda)
            listado = listado.filter(query)
        

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

            if nuevo_responsable:
                if Responsable.objects.filter(nombre=nuevo_responsable).exists():
                    messages.error(request, 'El responsable ya existe')
                    return redirect('/añadir/')
                else:
                    responsable = Responsable.objects.create(nombre=nuevo_responsable)
            else:
                responsable = Responsable.objects.get(id=responsable_id)

            if nueva_carrera:
                if Carrera.objects.filter(nombre=nueva_carrera).exists():
                    messages.error(request, 'La carrera ya existe')
                    return redirect('/añadir/')
                else:
                    carrera = Carrera.objects.create(nombre=nueva_carrera)
            else:
                carrera = Carrera.objects.get(id=carrera_id)

            if nueva_ubicacion:
                if Ubicacion.objects.filter(nombre=nueva_ubicacion).exists():
                    messages.error(request, 'La ubicación ya existe')
                    return redirect('/añadir/')
                else:
                    ubicacion = Ubicacion.objects.create(nombre=nueva_ubicacion)
            else:
                ubicacion = Ubicacion.objects.get(id=ubicacion_id)

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
            ubicaciones = Ubicacion.objects.all()
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
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            if archivo.name.endswith('.xlsx'):
                df = pd.read_excel(archivo)
                df.fillna("N/A", inplace=True)
                
                columnas_requeridas = ['Etiqueta', 'Numero_Serie', 'Descripcion_Equipamiento', 'Responsable', 'Carrera', 'Ubicacion']
                if not set(columnas_requeridas).issubset(df.columns):
                    return redirect("/error/")

                for index, row in df.iterrows():
                    etiqueta = row['Etiqueta']
                    numero_serie = row['Numero_Serie']
                    descripcion = row['Descripcion_Equipamiento']
                    observacion = row['Observacion']
    
                    responsable, creado_responsable = Responsable.objects.get_or_create(nombre=row.Responsable)
                    carrera, creado_carrera = Carrera.objects.get_or_create(nombre=row.Carrera)
                    ubicacion, creado_ubicacion = Ubicacion.objects.get_or_create(nombre=row.Ubicacion)
                    objeto, creado = Inventario.objects.get_or_create(
                        Etiqueta=etiqueta,
                        Numero_Serie=numero_serie,
                        Descripcion_Equipamiento=descripcion,
                        Responsable=responsable.nombre,
                        Carrera=carrera.nombre,
                        Ubicacion=ubicacion.nombre,
                        Observacion=observacion,
                        Digitador=request.user.username 
                    )
                    if creado:
                        objeto.save()

                return redirect("/exito/")
            else:
                return redirect("/error_archivo/")
    else:
        form = ImportForm()
    return render(request, 'core/importar.html', {'form': form})


def descargar(request):
    if request.user.is_authenticated:
        data = {
            'Etiqueta': ['E1', 'E2', 'E3'],
            'Numero_Serie': ['N1', 'N2', 'N3'],
            'Descripcion_Equipamiento': ['D1', 'D2', 'D3'],
            'Responsable': ['R1', 'R2', 'R3'],
            'Carrera': ['C1', 'C2', 'C3'],
            'Ubicacion': ['U1', 'U2', 'U3'],
            'Observacion': ['O1', 'O2', 'O3']
        }

        df = pd.DataFrame(data)
        nombre_archivo = "datos_inventario.xlsx"
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        df.to_excel(response, index=False)

        return response
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
            if Responsable.objects.filter(nombre=nombre).exists():
                messages.error(request, 'El responsable ya existe')
                return redirect('/añadir/')
            else:
                nuevo_responsable = Responsable(nombre=nombre)
                nuevo_responsable.save()
                messages.success(request, 'Responsable añadido correctamente')
                return redirect('/añadir/')
    else:
        return redirect('/login/')

def añadir_carrera(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nombre = request.POST.get('nueva_carrera')
            if Carrera.objects.filter(nombre=nombre).exists():
                messages.error(request, 'La carrera ya existe')
                return redirect('/añadir/')
            else:
                nueva_carrera = Carrera(nombre=nombre)
                nueva_carrera.save()
                messages.success(request, 'Carrera añadida correctamente')
                return redirect('/añadir/')
    else:
        return redirect('/login/')

def añadir_ubicacion(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nombre = request.POST.get('nueva_ubicacion')
            if Ubicacion.objects.filter(nombre=nombre).exists():
                messages.error(request, 'La ubicación ya existe')
                return redirect('/añadir/')
            else:
                nueva_ubicacion = Ubicacion(nombre=nombre)
                nueva_ubicacion.save()
                messages.success(request, 'Ubicación añadida correctamente')
                return redirect('/añadir/')
    else:
        return redirect('/login/')
    
def error(request):
    if request.user.is_authenticated:
        
        return render(request,"core/error.html", {'user': request.user})

def error_archivo(request):
    if request.user.is_authenticated:
        
        return render(request,"core/archivo_no_compatible.html", {'user': request.user})
    

def descargar_activos(request):
    if request.user.is_authenticated:
        activos = Inventario.objects.all()
        data = []
        for activo in activos:
            data.append({
                'Etiqueta': activo.Etiqueta,
                'Numero_Serie': activo.Numero_Serie,
                'Descripcion_Equipamiento': activo.Descripcion_Equipamiento,
                'Responsable': activo.Responsable,
                'Carrera': activo.Carrera,
                'Ubicacion': activo.Ubicacion,
                'Observacion': activo.Observacion,
                'Digitador': activo.Digitador
            })
        df = pd.DataFrame(data)
        nombre_archivo = "inventario.xlsx"
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        df.to_excel(response, index=False)

        return response
    else:
        return redirect('/login/')
