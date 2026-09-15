"""Validación del lado del servidor para los formularios de la Tarea 2.

Replica exactamente las mismas reglas que ya existían en el JavaScript de la
Tarea 1 (js/registro_usuario.js y js/registro_avistamiento.js), tal como
pide el enunciado ("mantener todas las validaciones realizadas con
Javascript" + validar también en el servidor). Nunca hay que confiar en que
el navegador ya validó: cualquiera puede mandar una petición POST directa
con curl o herramientas de desarrollador saltándose el JavaScript por
completo, así que estas reglas se vuelven a aplicar acá desde cero sobre los
datos crudos que llegan en la petición.

Cada función devuelve un diccionario {nombre_campo: mensaje_error}. Un
diccionario vacío significa que los datos son válidos.
"""

from datetime import datetime

import filetype

from config import EXTENSIONES_PERMITIDAS, TAMANO_MAXIMO_ARCHIVO, TIPOS_MIME_PERMITIDOS


def _texto(valor):
    """Normaliza cualquier valor de formulario a texto sin espacios sobrantes.
    request.form.get(...) ya devuelve str o None; esto solo evita
    reventar con .strip() si el campo no vino en el POST."""
    return (valor or "").strip()


def entero_o_none(valor):
    """Convierte un id recibido por formulario o querystring a int, o None si
    no es un entero válido. Así una petición manipulada con un id como
    "1 OR 1=1" o "abc" nunca llega a usarse en una consulta: simplemente no
    pasa la validación."""
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def validar_voluntario(datos, comuna_ids_validas):
    errores = {}

    nombre = _texto(datos.get("nombre"))
    if not nombre or len(nombre) < 2 or len(nombre) > 50:
        errores["nombre"] = "Nombre inválido (debe tener entre 2 y 50 caracteres)."

    apellido = _texto(datos.get("apellido"))
    if not apellido or len(apellido) < 2 or len(apellido) > 50:
        errores["apellido"] = "Apellido inválido (debe tener entre 2 y 50 caracteres)."

    correo = _texto(datos.get("correo"))
    # El límite superior es 80 porque así está definida la columna
    # voluntario.email (VARCHAR(80)) en tarea2.sql: un correo más largo
    # pasaría esta validación pero fallaría al insertarse en MySQL.
    if not correo or "@" not in correo or "." not in correo or len(correo) < 5 or len(correo) > 80:
        errores["correo"] = "Email inválido (máximo 80 caracteres)."

    telefono = _texto(datos.get("telefono"))
    solo_numeros = telefono.replace("+", "").replace(" ", "")
    if not telefono or not solo_numeros.isdigit() or len(telefono) > 15 or len(solo_numeros) < 8:
        errores["telefono"] = "Teléfono inválido (use solo números, entre 8 y 15 caracteres)."

    comuna_id = entero_o_none(datos.get("comuna"))
    if comuna_id is None or comuna_id not in comuna_ids_validas:
        errores["comuna"] = "Debes seleccionar una comuna válida."

    return errores


def validar_avistamiento(datos, voluntario_ids_validas, ave_ids_validas):
    errores = {}

    voluntario_id = entero_o_none(datos.get("voluntario"))
    if voluntario_id is None or voluntario_id not in voluntario_ids_validas:
        errores["voluntario"] = "Debes seleccionar un voluntario válido."

    ave_id = entero_o_none(datos.get("ave"))
    if ave_id is None or ave_id not in ave_ids_validas:
        errores["ave"] = "Debes seleccionar un ave válida."

    lugar = _texto(datos.get("lugar"))
    if not lugar or len(lugar) < 2 or len(lugar) > 100:
        errores["lugar"] = "Lugar inválido (debe tener entre 2 y 100 caracteres)."

    fecha = _texto(datos.get("fecha"))
    hora = _texto(datos.get("hora"))
    if not fecha or not hora:
        errores["fecha"] = "Debes ingresar la fecha y la hora."
    else:
        try:
            fecha_avistamiento = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            if fecha_avistamiento > datetime.now():
                errores["fecha"] = "La fecha del avistamiento no puede estar en el futuro."
        except ValueError:
            errores["fecha"] = "Formato de fecha u hora inválido."

    descripcion = _texto(datos.get("descripcion"))
    if len(descripcion) > 500:
        errores["descripcion"] = "La descripción no puede superar los 500 caracteres."

    return errores


def archivo_valido(archivo):
    """Verifica un único archivo subido (objeto FileStorage de Flask):
    extensión permitida, tamaño máximo y tipo real de contenido (no solo la
    extensión que declaró el navegador, que un usuario malicioso puede
    falsificar con facilidad). Devuelve (es_valido, mensaje_error)."""
    nombre = archivo.filename or ""
    if "." not in nombre:
        return False, "El archivo no tiene una extensión válida."

    extension = nombre.rsplit(".", 1)[1].lower()
    if extension not in EXTENSIONES_PERMITIDAS:
        return False, f'Formato "{extension}" no permitido (solo JPG, PNG o MP4).'

    archivo.stream.seek(0, 2)  # mover el cursor al final para medir el tamaño
    tamano = archivo.stream.tell()
    archivo.stream.seek(0)
    if tamano > TAMANO_MAXIMO_ARCHIVO:
        return False, f'El archivo "{nombre}" es demasiado pesado (máximo 5 MB).'
    if tamano == 0:
        return False, f'El archivo "{nombre}" está vacío.'

    tipo_real = filetype.guess(archivo.stream.read(261))
    archivo.stream.seek(0)
    if tipo_real is None or tipo_real.mime not in TIPOS_MIME_PERMITIDOS:
        return False, f'El contenido de "{nombre}" no corresponde a una imagen o video válido.'

    return True, ""
