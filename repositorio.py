"""Acceso a datos para la Tarea 2, usando SQLAlchemy tal como se enseñó en
5-python-sqlalchemy: create_engine + Session + select(). Cada función recibe
una Session ya abierta (la crea y cierra app.py con un bloque `with`, igual
que personas-flask.py) y hace exactamente una operación, para que las rutas
de app.py no mezclen SQL con lógica de la vista.
"""

from datetime import datetime

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, selectinload

from config import DATABASE_URL
from models import Avistamiento, Ave, Comuna, Region, Registro, Voluntario

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


def crear_avistamiento(sesion, voluntario_id, ave_id, fecha_hora, lugar, descripcion):
    avistamiento = Avistamiento(
        voluntario_id=voluntario_id,
        ave_id=ave_id,
        fecha_hora=fecha_hora,
        lugar=lugar,
        descripcion=descripcion or None,
    )
    sesion.add(avistamiento)
    sesion.commit()
    return avistamiento


def agregar_registro(sesion, avistamiento_id, ruta_archivo, nombre_archivo):
    registro = Registro(
        avistamiento_id=avistamiento_id,
        ruta_archivo=ruta_archivo,
        nombre_archivo=nombre_archivo,
    )
    sesion.add(registro)
    sesion.commit()
    return registro


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
        .options(selectinload(Avistamiento.ave), selectinload(Avistamiento.voluntario))
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
