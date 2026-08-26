"""Biblioteca — el usuario ya puede escribir en la base.

Las lecturas siguen siendo GET; toda escritura es POST y termina en un
redirect. Ese es el patron Post/Redirect/Get: si el usuario recarga con F5,
la ultima peticion del historial es un GET inofensivo y no se duplica nada.
"""
import os

from flask import Flask, flash, redirect, render_template, request, url_for

from models import db, Autor, Libro

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg://app:123qwe@localhost:5433/store'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'clave-de-desarrollo')

db.init_app(app)


@app.route('/')
def inicio():
    """La portada es el catalogo."""
    return listar_libros()


@app.route('/libros')
def listar_libros():
    """GET /libros  →  catalogo en HTML. Acepta ?autor=... para filtrar."""
    autor = request.args.get('autor', '')
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


@app.route('/libros/crear', methods=['GET', 'POST'])
def crear_libro():
    """GET  →  muestra el formulario vacio.
       POST →  inserta el libro y redirige al catalogo."""
    if request.method == 'GET':
        return render_template('libros/formulario.html', libro=None,
                               autores=Autor.query.order_by(Autor.nombre).all())

    try:
        libro = Libro(
            titulo=request.form['titulo'],
            anio=request.form.get('anio') or None,
            autor_id=request.form['autor_id'],
            disponible='disponible' in request.form,
        )
        db.session.add(libro)
        db.session.commit()
        flash('Libro creado.', 'exito')
    except Exception:
        db.session.rollback()
        flash('No se pudo crear el libro.', 'error')

    return redirect(url_for('listar_libros'))


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
