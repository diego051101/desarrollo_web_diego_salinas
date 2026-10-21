"""Modelos SQLAlchemy 2.0, mapeados 1 a 1 sobre las tablas creadas por
sql/tarea2.sql (region, comuna, voluntario, ave, avistamiento, registro) y
sql/tabla-comentario.sql (comentario). Sigue el mismo estilo enseñado en la
clase 5-python-sqlalchemy (DeclarativeBase + Mapped + mapped_column).

Solo se declaran como relationship() de SQLAlchemy los vínculos que el
código realmente navega (avistamiento.ave, avistamiento.voluntario,
avistamiento.registros, usados en las plantillas); el resto de las llaves
foráneas del diagrama (region_id, comuna_id) se usan como columnas simples,
sin necesitar el objeto relacionado completo.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Region(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200))


class Comuna(Base):
    __tablename__ = "comuna"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200))
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))


class Voluntario(Base):
    __tablename__ = "voluntario"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(80))
    telefono: Mapped[str] = mapped_column(String(15))
    fecha_registro: Mapped[datetime] = mapped_column(DateTime)
    comuna_id: Mapped[int] = mapped_column(ForeignKey("comuna.id"))


class Ave(Base):
    __tablename__ = "ave"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(80))


class Avistamiento(Base):
    __tablename__ = "avistamiento"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    voluntario_id: Mapped[int] = mapped_column(ForeignKey("voluntario.id"))
    ave_id: Mapped[int] = mapped_column(ForeignKey("ave.id"))
    fecha_hora: Mapped[datetime] = mapped_column(DateTime)
    lugar: Mapped[str] = mapped_column(String(200))
    descripcion: Mapped[Optional[str]] = mapped_column(Text(500), nullable=True)

    # Navegados directamente en las plantillas: avistamiento.ave.nombre,
    # avistamiento.voluntario.nombre, avistamiento.registros.
    ave: Mapped["Ave"] = relationship()
    voluntario: Mapped["Voluntario"] = relationship()
    registros: Mapped[List["Registro"]] = relationship(
        cascade="all, delete-orphan", order_by="Registro.id"
    )


class Registro(Base):
    __tablename__ = "registro"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ruta_archivo: Mapped[str] = mapped_column(String(300))
    nombre_archivo: Mapped[str] = mapped_column(String(300))
    avistamiento_id: Mapped[int] = mapped_column(ForeignKey("avistamiento.id"))

    @property
    def es_video(self) -> bool:
        """La plantilla de detalle necesita saber si debe usar <video> o <img>."""
        return self.nombre_archivo.lower().endswith(".mp4")

    @property
    def ruta_relativa(self) -> str:
        """Ruta dentro de static/ para construir la URL servible con
        url_for('static', filename=registro.ruta_relativa). Se calcula a
        partir de ruta_archivo + nombre_archivo en vez de repetir la
        concatenación en cada plantilla que muestra un archivo adjunto."""
        return f"{self.ruta_archivo}/{self.nombre_archivo}"


class Comentario(Base):
    __tablename__ = "comentario"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(80))
    texto: Mapped[str] = mapped_column(String(300))
    fecha: Mapped[datetime] = mapped_column(DateTime)
    avistamiento_id: Mapped[int] = mapped_column(ForeignKey("avistamiento.id"))
