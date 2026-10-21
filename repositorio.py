"""Acceso a datos del sitio, usando SQLAlchemy tal como se enseñó en
5-python-sqlalchemy: create_engine + Session + select(). Cada función recibe
una Session ya abierta (la crea y cierra app.py con un bloque `with`, igual
que personas-flask.py) y hace exactamente una operación, para que las rutas
de app.py no mezclen SQL con lógica de la vista.
"""

from datetime import datetime

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, selectinload

from config import DATABASE_URL
from models import Avistamiento, Ave, Comentario, Comuna, Region, Registro, Voluntario

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def crear_sesion():
    return Session(engine)


# --- Catálogos (región / comuna / ave / voluntario) ---------------------

def obtener_regiones(sesion):
    return list(sesion.scalars(select(Region).order_by(Region.nombre)))


def obtener_comunas(sesion):
    return list(sesion.scalars(select(Comuna).order_by(Comuna.nombre)))


def obtener_ids_comunas(sesion):
    return set(sesion.scalars(select(Comuna.id)))


def obtener_aves(sesion):
    return list(sesion.scalars(select(Ave).order_by(Ave.nombre)))


def obtener_ids_aves(sesion):
    return set(sesion.scalars(select(Ave.id)))


def obtener_voluntarios(sesion):
    return list(sesion.scalars(select(Voluntario).order_by(Voluntario.nombre)))


def obtener_ids_voluntarios(sesion):
    return set(sesion.scalars(select(Voluntario.id)))


# --- Escritura ------------------------------------------------------------

def crear_voluntario(sesion, nombre, email, telefono, comuna_id):
    voluntario = Voluntario(
        nombre=nombre,
        email=email,
        telefono=telefono,
        fecha_registro=datetime.now(),
        comuna_id=comuna_id,
    )
    sesion.add(voluntario)
    sesion.commit()
    return voluntario


def crear_avistamiento(sesion, voluntario_id, ave_id, fecha_hora, lugar, descripcion, nombres_archivo):
    """Guarda el avistamiento junto con una fila de registro por archivo en
    un único commit, para que nunca quede un avistamiento sin sus adjuntos."""
    avistamiento = Avistamiento(
        voluntario_id=voluntario_id,
        ave_id=ave_id,
        fecha_hora=fecha_hora,
        lugar=lugar,
        descripcion=descripcion or None,
        registros=[
            Registro(ruta_archivo="uploads", nombre_archivo=nombre) for nombre in nombres_archivo
        ],
    )
    sesion.add(avistamiento)
    sesion.commit()
    return avistamiento


def crear_comentario(sesion, avistamiento_id, nombre, texto):
    comentario = Comentario(
        avistamiento_id=avistamiento_id,
        nombre=nombre,
        texto=texto,
        fecha=datetime.now(),
    )
    sesion.add(comentario)
    sesion.commit()
    return comentario


# --- Lectura para portada / listado / detalle -----------------------------

def obtener_ultimos_avistamientos(sesion, cantidad=2):
    consulta = (
        select(Avistamiento)
        .options(selectinload(Avistamiento.ave), selectinload(Avistamiento.voluntario))
        .order_by(Avistamiento.fecha_hora.desc())
        .limit(cantidad)
    )
    return list(sesion.scalars(consulta))


def contar_avistamientos(sesion):
    return sesion.scalar(select(func.count(Avistamiento.id))) or 0


def obtener_avistamientos_paginados(sesion, pagina, por_pagina):
    consulta = (
        select(Avistamiento)
        .options(
            selectinload(Avistamiento.ave),
            selectinload(Avistamiento.voluntario),
            selectinload(Avistamiento.registros),
        )
        .order_by(Avistamiento.fecha_hora.desc())
        .limit(por_pagina)
        .offset((pagina - 1) * por_pagina)
    )
    return list(sesion.scalars(consulta))


def obtener_avistamiento_detalle(sesion, avistamiento_id):
    consulta = (
        select(Avistamiento)
        .options(
            selectinload(Avistamiento.ave),
            selectinload(Avistamiento.voluntario),
            selectinload(Avistamiento.registros),
        )
        .where(Avistamiento.id == avistamiento_id)
    )
    return sesion.scalars(consulta).first()


def existe_avistamiento(sesion, avistamiento_id):
    return sesion.get(Avistamiento, avistamiento_id) is not None


def obtener_comentarios(sesion, avistamiento_id):
    consulta = (
        select(Comentario)
        .where(Comentario.avistamiento_id == avistamiento_id)
        .order_by(Comentario.fecha.desc(), Comentario.id.desc())
    )
    return list(sesion.scalars(consulta))


# --- Estadísticas: cada función devuelve filas (etiqueta, cantidad) -------

def contar_avistamientos_por_dia(sesion):
    dia = func.date(Avistamiento.fecha_hora)
    consulta = select(dia, func.count(Avistamiento.id)).group_by(dia).order_by(dia)
    return sesion.execute(consulta).all()


def contar_avistamientos_por_ave(sesion):
    total = func.count(Avistamiento.id)
    consulta = (
        select(Ave.nombre, total)
        .join(Avistamiento, Avistamiento.ave_id == Ave.id)
        .group_by(Ave.id, Ave.nombre)
        .order_by(total.desc(), Ave.nombre)
    )
    return sesion.execute(consulta).all()


def contar_voluntarios_por_comuna(sesion):
    consulta = (
        select(Comuna.nombre, func.count(Voluntario.id))
        .join(Voluntario, Voluntario.comuna_id == Comuna.id)
        .group_by(Comuna.id, Comuna.nombre)
        .order_by(Comuna.nombre)
    )
    return sesion.execute(consulta).all()
