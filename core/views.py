from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from .models import Inventario,Responsable,Carrera,Ubicacion
from django.db.models import Q
from .forms import ImportForm
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from openpyxl import Workbook
from django.views.decorators.http import require_POST



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
        termino_busqueda = request.GET.get('buscar', '')
        responsable = request.GET.get('Responsable', None)
        carrera = request.GET.get('Carrera', None)
        ubicacion = request.GET.get('Ubicacion', None)

        listado = filtrar_datos(request, termino_busqueda, responsable, carrera, ubicacion)
        
        responsables = Responsable.objects.all()
        carreras = Carrera.objects.all()
        ubicaciones = Ubicacion.objects.all()
        context = {
            'responsables': responsables,
            'carreras': carreras,
            'ubicaciones': ubicaciones,
            'termino_busqueda': termino_busqueda,
            'responsable_seleccionado': responsable,
            'carrera_seleccionada': carrera,
            'ubicacion_seleccionada': ubicacion,
            'listado': listado,
            'user': request.user,
        }
        return render(request, 'core/listar.html', context)
    else:
        return redirect('/login/')

def obtener_listado_actualizado(request):
    listado_actualizado = Inventario.objects.all().values()
    listado_serializado = list(listado_actualizado)
    return JsonResponse(listado_serializado, safe=False)

def añadir(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            responsable_id = request.POST.get('responsable')
            carrera_id = request.POST.get('carrera')
            ubicacion_id = request.POST.get('ubicacion')
            nuevo_responsable = request.POST.get('nuevo_responsable')
            nueva_carrera = request.POST.get('nueva_carrera')
            nueva_ubicacion = request.POST.get('nueva_ubicacion')
            
            # Función para asignar "N/A" si el campo está vacío
            def asignar_na(valor):
                return valor if valor else "N/A"

            # Manejo de responsable
            if nuevo_responsable:
                if Responsable.objects.filter(nombre=nuevo_responsable).exists():
                    messages.error(request, 'El responsable ya existe')
                    return redirect('/añadir/')
                else:
                    responsable = Responsable.objects.create(nombre=nuevo_responsable)
            else:
                responsable = Responsable.objects.get(id=responsable_id)

            # Manejo de carrera
            if nueva_carrera:
                if Carrera.objects.filter(nombre=nueva_carrera).exists():
                    messages.error(request, 'La carrera ya existe')
                    return redirect('/añadir/')
                else:
                    carrera = Carrera.objects.create(nombre=nueva_carrera)
            else:
                carrera = Carrera.objects.get(id=carrera_id)

            # Manejo de ubicación
            if nueva_ubicacion:
                if Ubicacion.objects.filter(nombre=nueva_ubicacion).exists():
                    messages.error(request, 'La ubicación ya existe')
                    return redirect('/añadir/')
                else:
                    ubicacion = Ubicacion.objects.create(nombre=nueva_ubicacion)
            else:
                ubicacion = Ubicacion.objects.get(id=ubicacion_id)

            etiquetas = request.POST.getlist('etiqueta[]')
            numeros_serie = request.POST.getlist('numero_serie[]')
            descripciones = request.POST.getlist('descripcion_equipamiento[]')
            observaciones = request.POST.getlist('observacion[]')

            for etiqueta, numero_serie, descripcion, observacion in zip(etiquetas, numeros_serie, descripciones, observaciones):
                # Asignar "N/A" si los campos vienen vacíos
                etiqueta = asignar_na(etiqueta)
                numero_serie = asignar_na(numero_serie)
                descripcion = asignar_na(descripcion)
                observacion = asignar_na(observacion)

                if etiqueta != "N/A" and Inventario.objects.filter(Etiqueta=etiqueta).exists():
                    messages.error(request, f'La etiqueta "{etiqueta}" ya ha sido utilizada. Por favor, elija otra.')
                    return redirect('/añadir/')
                if numero_serie != "N/A" and Inventario.objects.filter(Numero_Serie=numero_serie).exists():
                    messages.error(request, f'El número de serie "{numero_serie}" ya ha sido utilizado. Por favor, elija otro.')
                    return redirect('/añadir/')
                
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

            messages.success(request, 'Equipamientos añadidos exitosamente.')
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
                etiquetas_existente = set(Inventario.objects.values_list('Etiqueta', flat=True))
                numeros_serie_existente = set(Inventario.objects.values_list('Numero_Serie', flat=True))

                for index, row in df.iterrows():
                    etiqueta = row['Etiqueta']
                    numero_serie = row['Numero_Serie']

                    if etiqueta in etiquetas_existente:
                        return redirect("/error_etiqueta/")
                    if numero_serie in numeros_serie_existente:
                        return redirect("/error_numero_serie/")

                    responsable, creado_responsable = Responsable.objects.get_or_create(nombre=row.Responsable)
                    carrera, creado_carrera = Carrera.objects.get_or_create(nombre=row.Carrera)
                    ubicacion, creado_ubicacion = Ubicacion.objects.get_or_create(nombre=row.Ubicacion)
                    objeto, creado = Inventario.objects.get_or_create(
                        Etiqueta=etiqueta,
                        Numero_Serie=numero_serie,
                        Descripcion_Equipamiento=row['Descripcion_Equipamiento'],
                        Responsable=responsable.nombre,
                        Carrera=carrera.nombre,
                        Ubicacion=ubicacion.nombre,
                        Observacion=row['Observacion'],
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
            nombre = request.POST.get('nuevo_responsable').strip().upper() 
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
            nombre = request.POST.get('nueva_carrera').strip().upper() 
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
            nombre = request.POST.get('nueva_ubicacion').strip().upper() 
            if Ubicacion.objects.filter(nombre=nombre).exists():
                messages.ERROR(request, 'La ubicación ya existe')
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

def error_Etiqueta(request):
    if request.user.is_authenticated:
        
        return render(request,"core/error_etiqueta.html", {'user': request.user})
    
def error_numero_serie(request):
    if request.user.is_authenticated:
        
        return render(request,"core/error_numero_serie.html", {'user': request.user})

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

def eliminar_elemento(request, elemento_id):
    elemento = get_object_or_404(Inventario, id=elemento_id)
    elemento.delete()
    return JsonResponse({'mensaje': 'El elemento ha sido eliminado correctamente'})

def filtrar_datos(request, termino_busqueda, responsable=None, carrera=None, ubicacion=None):
    queryset = Inventario.objects.all().order_by('-id')

    if termino_busqueda:
        queryset = queryset.filter(
            Q(Etiqueta__icontains=termino_busqueda) |
            Q(Numero_Serie__icontains=termino_busqueda) |
            Q(Descripcion_Equipamiento__icontains=termino_busqueda) |
            Q(Responsable__icontains=termino_busqueda) |
            Q(Carrera__icontains=termino_busqueda) |
            Q(Ubicacion__icontains=termino_busqueda) |
            Q(Observacion__icontains=termino_busqueda) |
            Q(Digitador__icontains=termino_busqueda)
        )

    if responsable:
        queryset = queryset.filter(Responsable__icontains=responsable)

    if carrera:
        queryset = queryset.filter(Carrera__icontains=carrera)

    if ubicacion:
        queryset = queryset.filter(Ubicacion__icontains=ubicacion)

    return queryset



def modificar_activo(request, item_id):

    return redirect('lista')

def exportar_excel(request):
    if request.user.is_authenticated:
        responsable = request.GET.get('Responsable')
        carrera = request.GET.get('Carrera')
        ubicacion = request.GET.get('Ubicacion')
        termino_busqueda = request.GET.get('buscar', '')

        listado_filtrado = filtrar_datos(request, termino_busqueda, responsable, carrera, ubicacion)

        # Crea un nuevo libro de trabajo de Excel
        workbook = Workbook()
        sheet = workbook.active
        encabezados = [
            'Codigo_USM',
            'Numero_Serie',
            'Descripcion_Equipamiento',
            'Responsable',
            'Carrera',
            'Ubicacion',
            'Observacion',
            'Digitador'
        ]

        sheet.append(encabezados)
        for item in listado_filtrado:
            fila = [
                item.Etiqueta,
                item.Numero_Serie,
                item.Descripcion_Equipamiento,
                item.Responsable,
                item.Carrera,
                item.Ubicacion,
                item.Observacion,
                item.Digitador
            ]
            sheet.append(fila)

        nombre_archivo = "ListaFiltrada.xlsx"
        if termino_busqueda:
            nombre_archivo = f"ListaFiltrada-{termino_busqueda}.xlsx"
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
        workbook.save(response)

        return response
    else:
        return redirect('/login/')



def modificar_activo(request, item_id):
    if request.method == 'POST':

        try:
            item = Inventario.objects.get(id=item_id)
        except Inventario.DoesNotExist:
            return redirect('error_page') 


        item.Etiqueta = request.POST.get('Etiqueta')
        item.Numero_Serie = request.POST.get('Numero_Serie')
        item.Descripcion_Equipamiento = request.POST.get('Descripcion_Equipamiento')
        item.Responsable = request.POST.get('Responsable')
        item.Carrera = request.POST.get('Carrera')
        item.Ubicacion = request.POST.get('Ubicacion')
        item.Observacion = request.POST.get('Observacion')
        item.Digitador = request.POST.get('Digitador')


        item.save()

        return redirect('lista')

    else:
        return redirect('error_page')
    
def borrar_activos(request):
    if request.user.is_authenticated:
        termino_busqueda = request.GET.get('buscar', '')
        responsable = request.GET.get('Responsable', None)
        carrera = request.GET.get('Carrera', None)
        ubicacion = request.GET.get('Ubicacion', None)

        listado = filtrar_datos(request, termino_busqueda, responsable, carrera, ubicacion)
        
        responsables = Responsable.objects.all()
        carreras = Carrera.objects.all()
        ubicaciones = Ubicacion.objects.all()
        context = {
            'responsables': responsables,
            'carreras': carreras,
            'ubicaciones': ubicaciones,
            'termino_busqueda': termino_busqueda,
            'responsable_seleccionado': responsable,
            'carrera_seleccionada': carrera,
            'ubicacion_seleccionada': ubicacion,
            'listado': listado,
            'user': request.user,
        }
        return render(request, 'core/borrar.html', context)
    else:
        return redirect('/login/')
def borrar_masivo(request):
    if request.method == 'POST':
        activos_seleccionados = request.POST.getlist('activos_seleccionados')  # Obtener la lista de activos seleccionados
        
        for id_activo in activos_seleccionados:
            try:
                activo = Inventario.objects.get(id=id_activo)
                activo.delete()  # Eliminar el activo de la base de datos
            except Inventario.DoesNotExist:
                pass  # Manejar el caso donde el activo no existe (opcional)

        # Después de borrar, redireccionar a la página de listado actualizada
        return redirect('/lista/')  # Cambia '/lista/' por tu URL de listado actual
    else:
        return redirect('/error/')