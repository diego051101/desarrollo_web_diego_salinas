"""Observatorio Digital Aviario, aplicación Flask de las Tareas 2 y 3.

Tarea 2: portada con últimos avistamientos, registro de voluntarios,
registro de avistamientos con archivos adjuntos y listado paginado con vista
de detalle. Tarea 3: estadísticas con gráficos generados en el navegador y
comentarios en cada avistamiento, ambos consumiendo las rutas /api/ con
fetch.

Sigue el mismo estilo de rutas que las clases del curso (una función por
ruta, render_template con las variables que la plantilla necesita), pero
separa en módulos propios la configuración, los modelos, el acceso a datos y
las validaciones, para que este archivo solo coordine la petición HTTP con
la respuesta.
"""

import math
import os
import uuid
from datetime import date, datetime, timedelta

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

import repositorio
from config import (
    AVISTAMIENTOS_POR_PAGINA,
    CARPETA_SUBIDAS,
    LARGO_NOMBRE_COMENTARIO,
    LARGO_TEXTO_COMENTARIO,
    MAX_CONTENT_LENGTH,
    SECRET_KEY,
)
from validaciones import (
    entero_o_none,
    validar_archivos,
    validar_avistamiento,
    validar_comentario,
    validar_voluntario,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(CARPETA_SUBIDAS, exist_ok=True)


def _mapa_comunas_por_region(sesion):
    """Agrupa las comunas por región para imprimirlas como JSON en la
    plantilla (ver static/js/registrar_voluntario.js)."""
    mapa = {}
    for comuna in repositorio.obtener_comunas(sesion):
        mapa.setdefault(str(comuna.region_id), []).append({"id": comuna.id, "nombre": comuna.nombre})
    return mapa


def _guardar_archivo(archivo):
    """Guarda el adjunto con un prefijo aleatorio para que dos archivos con el
    mismo nombre no se pisen, y devuelve el nombre final en disco."""
    nombre_unico = f"{uuid.uuid4().hex}_{secure_filename(archivo.filename)}"
    archivo.save(os.path.join(CARPETA_SUBIDAS, nombre_unico))
    return nombre_unico


# --- Páginas ---------------------------------------------------------------

@app.route("/")
def portada():
    with repositorio.crear_sesion() as sesion:
        ultimos_avistamientos = repositorio.obtener_ultimos_avistamientos(sesion, cantidad=2)
        return render_template("portada.html", ultimos_avistamientos=ultimos_avistamientos)


@app.route("/voluntarios/nuevo", methods=["GET", "POST"])
def nuevo_voluntario():
    with repositorio.crear_sesion() as sesion:
        contexto = {
            "regiones": repositorio.obtener_regiones(sesion),
            "comunas_por_region": _mapa_comunas_por_region(sesion),
            "errores": {},
            "valores": {},
            "voluntario_creado": None,
        }
        if request.method == "GET":
            return render_template("registrar_voluntario.html", **contexto)

        errores = validar_voluntario(request.form, repositorio.obtener_ids_comunas(sesion))
        if errores:
            contexto.update(errores=errores, valores=request.form)
            return render_template("registrar_voluntario.html", **contexto), 400

        contexto["voluntario_creado"] = repositorio.crear_voluntario(
            sesion,
            nombre=f"{request.form['nombre'].strip()} {request.form['apellido'].strip()}",
            email=request.form["correo"].strip(),
            telefono=request.form["telefono"].strip(),
            comuna_id=int(request.form["comuna"]),
        )
        return render_template("registrar_voluntario.html", **contexto)


@app.route("/avistamientos/nuevo", methods=["GET", "POST"])
def nuevo_avistamiento():
    with repositorio.crear_sesion() as sesion:
        contexto = {
            "voluntarios": repositorio.obtener_voluntarios(sesion),
            "aves": repositorio.obtener_aves(sesion),
            "errores": {},
            "valores": {"voluntario": request.args.get("voluntario_id", "")},
        }
        if request.method == "GET":
            return render_template("informar_avistamiento.html", **contexto)

        errores = validar_avistamiento(
            request.form,
            repositorio.obtener_ids_voluntarios(sesion),
            repositorio.obtener_ids_aves(sesion),
        )
        archivos = [archivo for archivo in request.files.getlist("archivos") if archivo.filename]
        error_archivos = validar_archivos(archivos)
        if error_archivos:
            errores["archivos"] = error_archivos

        if errores:
            contexto.update(errores=errores, valores=request.form)
            return render_template("informar_avistamiento.html", **contexto), 400

        repositorio.crear_avistamiento(
            sesion,
            voluntario_id=int(request.form["voluntario"]),
            ave_id=int(request.form["ave"]),
            fecha_hora=datetime.strptime(f"{request.form['fecha']} {request.form['hora']}", "%Y-%m-%d %H:%M"),
            lugar=request.form["lugar"].strip(),
            descripcion=request.form.get("descripcion", "").strip(),
            nombres_archivo=[_guardar_archivo(archivo) for archivo in archivos],
        )
        flash("¡Avistamiento registrado con éxito!", "exito")
        return redirect(url_for("portada"))


@app.route("/avistamientos")
def listado_avistamientos():
    with repositorio.crear_sesion() as sesion:
        total = repositorio.contar_avistamientos(sesion)
        total_paginas = max(1, math.ceil(total / AVISTAMIENTOS_POR_PAGINA))
        pagina_solicitada = entero_o_none(request.args.get("pagina")) or 1
        pagina = max(1, min(pagina_solicitada, total_paginas))
        avistamientos = repositorio.obtener_avistamientos_paginados(
            sesion, pagina, AVISTAMIENTOS_POR_PAGINA
        )
        return render_template(
            "listado_avistamientos.html",
            avistamientos=avistamientos,
            pagina=pagina,
            total_paginas=total_paginas,
        )


@app.route("/avistamientos/<int:avistamiento_id>")
def detalle_avistamiento(avistamiento_id):
    with repositorio.crear_sesion() as sesion:
        avistamiento = repositorio.obtener_avistamiento_detalle(sesion, avistamiento_id)
        if avistamiento is None:
            abort(404)
        return render_template(
            "detalle_avistamiento.html",
            avistamiento=avistamiento,
            largo_nombre=LARGO_NOMBRE_COMENTARIO,
            largo_texto=LARGO_TEXTO_COMENTARIO,
        )


@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("error_404.html"), 404


# --- API JSON consumida con fetch desde static/js/ --------------------------

def _serie(filas):
    """Convierte filas (etiqueta, cantidad) en las dos listas paralelas que
    necesita cada gráfico de static/js/estadisticas.js."""
    return {
        "etiquetas": [etiqueta for etiqueta, _ in filas],
        "valores": [cantidad for _, cantidad in filas],
    }


def _completar_dias(filas):
    """Agrega con cantidad 0 los días sin avistamientos entre el primero y el
    último, para que el gráfico de líneas no una dos días lejanos como si
    fueran consecutivos. MySQL devuelve DATE() como objeto date y SQLite como
    texto ISO, así que se normaliza pasando por str."""
    conteo = {date.fromisoformat(str(dia)): cantidad for dia, cantidad in filas}
    if not conteo:
        return []
    primer_dia = min(conteo)
    dias = [primer_dia + timedelta(days=n) for n in range((max(conteo) - primer_dia).days + 1)]
    return [(dia.strftime("%d/%m/%Y"), conteo.get(dia, 0)) for dia in dias]


def _comentario_json(comentario):
    return {
        "nombre": comentario.nombre,
        "texto": comentario.texto,
        "fecha": comentario.fecha.strftime("%d/%m/%Y %H:%M"),
        "fecha_iso": comentario.fecha.isoformat(timespec="minutes"),
    }


@app.route("/api/estadisticas")
def api_estadisticas():
    with repositorio.crear_sesion() as sesion:
        por_dia = _completar_dias(repositorio.contar_avistamientos_por_dia(sesion))
        return jsonify(
            avistamientos_por_dia=_serie(por_dia),
            avistamientos_por_ave=_serie(repositorio.contar_avistamientos_por_ave(sesion)),
            voluntarios_por_comuna=_serie(repositorio.contar_voluntarios_por_comuna(sesion)),
        )


@app.route("/api/avistamientos/<int:avistamiento_id>/comentarios", methods=["GET", "POST"])
def api_comentarios(avistamiento_id):
    with repositorio.crear_sesion() as sesion:
        if not repositorio.existe_avistamiento(sesion, avistamiento_id):
            return jsonify(error="El avistamiento no existe."), 404

        if request.method == "GET":
            comentarios = repositorio.obtener_comentarios(sesion, avistamiento_id)
            return jsonify(comentarios=[_comentario_json(comentario) for comentario in comentarios])

        errores = validar_comentario(request.form)
        if errores:
            return jsonify(errores=errores), 422

        comentario = repositorio.crear_comentario(
            sesion,
            avistamiento_id=avistamiento_id,
            nombre=request.form["nombre"].strip(),
            texto=request.form["texto"].strip(),
        )
        return jsonify(comentario=_comentario_json(comentario)), 201


if __name__ == "__main__":
    app.run(debug=True)
