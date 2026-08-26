"""Biblioteca — ahora las rutas devuelven HTML.

render_template busca el archivo bajo templates/, lo rellena con los datos
que le pasa la ruta y devuelve texto HTML. La plantilla no consulta la base:
la ruta consulta y le entrega los objetos ya listos.
"""
import os

from flask import Flask, render_template, request

from models import db, Autor, Libro

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg://app:123qwe@localhost:5433/store'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def inicio():
    """La portada es el catalogo."""
    return listar_libros()


@app.route('/libros')
def listar_libros():
    """GET /libros  →  catalogo en HTML. Acepta ?autor=... para filtrar."""
    autor = request.args.get('autor', '')      # lectura → request.args
    consulta = Libro.query

    if autor:
        consulta = consulta.join(Autor).filter(
            Autor.nombre.ilike(f'%{autor}%'))

    return render_template(
        'libros/index.html',
        libros=consulta.order_by(Libro.titulo).all(),
        filtro_autor=autor,
    )


@app.route('/libros/<int:libro_id>')
def detalle_libro(libro_id):
    """GET /libros/3  →  ficha del libro, o 404."""
    libro = Libro.query.get_or_404(libro_id)
    return render_template('libros/detalle.html', libro=libro)


@app.route('/autores')
def listar_autores():
    """GET /autores  →  autores con su cantidad de libros."""
    return render_template('autores/index.html',
                           autores=Autor.query.order_by(Autor.nombre).all())


@app.route('/autores/<int:autor_id>')
def detalle_autor(autor_id):
    """GET /autores/3  →  el autor y sus libros."""
    autor = Autor.query.get_or_404(autor_id)
    return render_template('autores/detalle.html', autor=autor)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
