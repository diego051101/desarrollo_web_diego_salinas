"""Tarea 2 — Observatorio Digital Aviario.

Aplicación Flask que implementa las funcionalidades pedidas en el enunciado
de la Tarea 2: portada con últimos avistamientos, registro de voluntarios,
registro de avistamientos con archivos adjuntos, y listado paginado con
vista de detalle — todo leyendo y escribiendo en MySQL a través de
SQLAlchemy (repositorio.py), con validación repetida en el servidor
(validaciones.py) además de la que ya existía en JavaScript.

Sigue el mismo estilo de rutas que las clases 3 a 6 del curso (una función
por ruta, methods=['GET', 'POST'] cuando corresponde, render_template con
las variables que la plantilla necesita) pero separando en módulos propios
la configuración, los modelos, el acceso a datos y las validaciones, para
que este archivo se dedique solo a coordinar la petición HTTP con la
respuesta — nada de SQL ni de reglas de validación vive aquí.
"""

import math
import os
import uuid
from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

import repositorio
from config import AVISTAMIENTOS_POR_PAGINA, CARPETA_SUBIDAS, MAX_CONTENT_LENGTH, SECRET_KEY
from validaciones import archivo_valido, entero_o_none, validar_avistamiento, validar_voluntario

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(CARPETA_SUBIDAS, exist_ok=True)


def _mapa_comunas_por_region(sesion):
    """Agrupa las comunas por región y las deja listas para imprimirse como
    JSON en la plantilla (ver static/js/registrar_voluntario.js), en vez de
    que el navegador tenga que pedirlas con fetch como en la Tarea 1."""
    mapa = {}
    for comuna in repositorio.obtener_comunas(sesion):
        mapa.setdefault(str(comuna.region_id), []).append({"id": comuna.id, "nombre": comuna.nombre})
    return mapa


@app.route("/")
def portada():
    with repositorio.crear_sesion() as sesion:
        ultimos_avistamientos = repositorio.obtener_ultimos_avistamientos(sesion, cantidad=2)
        return render_template("portada.html", ultimos_avistamientos=ultimos_avistamientos)


@app.route("/voluntarios/nuevo", methods=["GET", "POST"])
def nuevo_voluntario():
    with repositorio.crear_sesion() as sesion:
        regiones = repositorio.obtener_regiones(sesion)
        comunas_por_region = _mapa_comunas_por_region(sesion)

        if request.method == "POST":
            comuna_ids_validas = repositorio.obtener_ids_comunas(sesion)
            errores = validar_voluntario(request.form, comuna_ids_validas)

            if errores:
                return render_template(
                    "registrar_voluntario.html",
                    regiones=regiones,
                    comunas_por_region=comunas_por_region,
                    errores=errores,
                    valores=request.form,
                    voluntario_creado=None,
                ), 400

            nombre_completo = f"{request.form['nombre'].strip()} {request.form['apellido'].strip()}"
            voluntario = repositorio.crear_voluntario(
                sesion,
                nombre=nombre_completo,
                email=request.form["correo"].strip(),
                telefono=request.form["telefono"].strip(),
                comuna_id=int(request.form["comuna"]),
            )
            return render_template(
                "registrar_voluntario.html",
                regiones=regiones,
                comunas_por_region=comunas_por_region,
                errores={},
                valores={},
                voluntario_creado=voluntario,
            )

        return render_template(
            "registrar_voluntario.html",
            regiones=regiones,
            comunas_por_region=comunas_por_region,
            errores={},
            valores={},
            voluntario_creado=None,
        )


@app.route("/avistamientos/nuevo", methods=["GET", "POST"])
def nuevo_avistamiento():
    with repositorio.crear_sesion() as sesion:
        voluntarios = repositorio.obtener_voluntarios(sesion)
        aves = repositorio.obtener_aves(sesion)

        if request.method == "POST":
            errores = validar_avistamiento(
                request.form,
                repositorio.obtener_ids_voluntarios(sesion),
                repositorio.obtener_ids_aves(sesion),
            )

            archivos = [archivo for archivo in request.files.getlist("archivos") if archivo.filename]
            if not archivos:
                errores["archivos"] = "Debes adjuntar al menos una fotografía o video."
            else:
                for archivo in archivos:
                    valido, mensaje = archivo_valido(archivo)
                    if not valido:
                        errores["archivos"] = mensaje
                        break

            if errores:
                return render_template(
                    "informar_avistamiento.html",
                    voluntarios=voluntarios,
                    aves=aves,
                    errores=errores,
                    valores=request.form,
                ), 400

            fecha_hora = datetime.strptime(
                f"{request.form['fecha']} {request.form['hora']}", "%Y-%m-%d %H:%M"
            )
            avistamiento = repositorio.crear_avistamiento(
                sesion,
                voluntario_id=int(request.form["voluntario"]),
                ave_id=int(request.form["ave"]),
                fecha_hora=fecha_hora,
                lugar=request.form["lugar"].strip(),
                descripcion=request.form.get("descripcion", "").strip(),
            )

            for archivo in archivos:
                nombre_unico = f"{uuid.uuid4().hex}_{secure_filename(archivo.filename)}"
                archivo.save(os.path.join(CARPETA_SUBIDAS, nombre_unico))
                repositorio.agregar_registro(
                    sesion,
                    avistamiento_id=avistamiento.id,
                    ruta_archivo="uploads",
                    nombre_archivo=nombre_unico,
                )

            flash("¡Avistamiento registrado con éxito!", "exito")
            return redirect(url_for("portada"))

        return render_template(
            "informar_avistamiento.html",
            voluntarios=voluntarios,
            aves=aves,
            errores={},
            valores={"voluntario": request.args.get("voluntario_id", "")},
        )


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
        return render_template("detalle_avistamiento.html", avistamiento=avistamiento)


@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("error_404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
