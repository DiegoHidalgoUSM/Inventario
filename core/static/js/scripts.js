function guardarCambios(event) {
    event.preventDefault();  // Evitar el envío del formulario estándar
    var form = document.getElementById('formModificarActivo');
    var data = new FormData(form);
    var itemId = document.getElementById('modificar_id').value;  // Obtener el ID del elemento a modificar
    enviarDatosModificacion(data, itemId);  // Pasar el ID del elemento como argumento
}

function enviarDatosModificacion(data, itemId) {
    fetch(`/modificar-activo/${itemId}/`, {
        method: 'POST',
        body: data,
        headers: {'X-CSRFToken': '{{ csrf_token }}'}
    })
    .then(response => {
        if (response.ok) {
            // Mostrar mensaje de éxito
            alert('Datos modificados correctamente');
            
            // Preguntar al usuario si desea recargar la página
            if (confirm('¿Desea recargar la página para ver los cambios?')) {
                location.reload(); // Recargar la página
            } else {
                cerrarModal('modificar');
                actualizarListado(); // Actualizar el listado después de cerrar el modal
            }
        } else {
            console.error('Error al modificar datos');
        }
    })
    .catch(error => {
        console.error('Error de red:', error);
    });
}


function abrirModal(tipo) {
    document.getElementById('modal' + capitalizeFirstLetter(tipo)).style.display = 'block';
}

function cerrarModal(tipo) {
    document.getElementById('modal' + capitalizeFirstLetter(tipo)).style.display = 'none';
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function abrirModalModificar(id, etiqueta, numeroSerie, descripcion, responsable, carrera, ubicacion, observacion, digitador) {
    document.getElementById('modificar_id').value = id;
    document.getElementById('modificar_etiqueta').value = etiqueta;
    document.getElementById('modificar_numero_serie').value = numeroSerie;
    document.getElementById('modificar_descripcion').value = descripcion;
    document.getElementById('modificar_responsable').value = responsable;
    document.getElementById('modificar_carrera').value = carrera;
    document.getElementById('modificar_ubicacion').value = ubicacion;
    document.getElementById('modificar_observacion').value = observacion;
    document.getElementById('modificar_digitador').value = digitador;
    abrirModal('modificar');
}

function exportarExcel() {
    var url = "{% url 'exportar_excel' %}";
    var filtros = JSON.parse(sessionStorage.getItem('filtros')) || [];
    var termino_busqueda = sessionStorage.getItem('termino_busqueda') || '';
    if (filtros.length > 0 || termino_busqueda) {
        url += "?";
        if (filtros.length > 0) {
            url += "filtro=" + filtros.join("&filtro=");
        }
        if (termino_busqueda) {
            url += (filtros.length > 0 ? "&" : "") + "buscar=" + encodeURIComponent(termino_busqueda);
        }
    }
    window.location.href = url;
}

function eliminarItem(itemId) {
    if (window.confirm("¿Seguro que desea borrar en la lista?")) {
        fetch(`/eliminar/${itemId}/`, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json','X-CSRFToken': '{{ csrf_token }}'},
        })
        .then(response => {
            if (response.ok) {
                console.log('Elemento eliminado correctamente');
                window.confirm("Se ha borrado elemento de la lista");
                window.location.href = "/lista/";
            } else {
                console.error('Error al eliminar elemento');
            }
        })
        .catch(error => {
            console.error('Error de red:', error);
        });
    }
}

function mostrarSelect(checkbox) {
    var selectId = 'select' + checkbox.value;
    var select = document.getElementById(selectId);
    if (checkbox.checked) {
        select.style.display = 'block';
    } else {
        select.style.display = 'none';
    }
}

function guardarFiltros(event) {
    event.preventDefault();  // Evita el envío del formulario estándar
    var form = document.getElementById('filtroForm');
    var data = new FormData(form);
    var buscar = data.get('buscar');
    var url = new URL(window.location.href);
    var params = url.searchParams;

    // Limpiar parámetros anteriores
    params.delete('filtro');
    params.delete('buscar');
    params.delete('Responsable');
    params.delete('Carrera');
    params.delete('Ubicacion');

    // Añadir término de búsqueda
    if (buscar) {
        params.set('buscar', buscar);
    }

    // Añadir filtros específicos si están seleccionados
    if (data.has('filtro')) {
        data.getAll('filtro').forEach(filtro => {
            var select = document.getElementById('select' + filtro);
            if (select && select.style.display !== 'none' && select.value) {
                params.append(filtro, select.value);
            }
        });
    }

    // Redirige a la URL con los parámetros de filtro
    window.location.href = url.toString();
}

function mostrarSeccion2() {
    document.getElementById('seccion1').classList.remove('active');
    document.getElementById('seccion2').classList.add('active');
}

function mostrarSeccion1() {
    document.getElementById('seccion2').classList.remove('active');
    document.getElementById('seccion1').classList.add('active');
}

document.getElementById('formulario').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir envío automático del formulario
    
    // Obtener los valores de número de serie y etiqueta
    const numeroSerie = document.getElementById('numero_serie').value;
    const etiqueta = document.getElementById('etiqueta').value;
    
    // Realizar la validación
    if (esRepetido(numeroSerie, 'numero_serie')) {
        alert('El número de serie ya ha sido utilizado. Por favor, elija otro.');
        return;
    }
    
    if (esRepetido(etiqueta, 'etiqueta')) {
        alert('La etiqueta ya ha sido utilizada. Por favor, elija otra.');
        return;
    }
    
    // Si la validación es exitosa, enviar el formulario
    this.submit();
});

function esRepetido(valor, campo) {
    // Obtener todos los elementos del formulario con el mismo valor
    const elementosConValor = document.querySelectorAll(`input[name=${campo}][value="${valor}"]`);
    
    // Si hay más de un elemento con el mismo valor, significa que ya se ha utilizado
    return elementosConValor.length > 1;
}