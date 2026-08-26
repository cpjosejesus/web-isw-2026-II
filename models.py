"""Modelos de la biblioteca: un autor tiene muchos libros.

La llave foranea vive del lado `muchos` (Libro.autor_id). La relacion
`Autor.libros` no es una columna: es un atajo del ORM.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Autor(db.Model):
    __tablename__ = 'autores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    nacionalidad = db.Column(db.String(80))

    libros = db.relationship('Libro', backref='autor',
                             lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Autor id={self.id} nombre={self.nombre}>'

    def format(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'nacionalidad': self.nacionalidad,
            'libros': len(self.libros),
        }


class Libro(db.Model):
    __tablename__ = 'libros'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    anio = db.Column(db.Integer)
    disponible = db.Column(db.Boolean, nullable=False, default=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'),
                         nullable=False)

    def __repr__(self):
        return f'<Libro id={self.id} titulo={self.titulo}>'

    def format(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'anio': self.anio,
            'disponible': self.disponible,
            'autor': self.autor.nombre,
        }
