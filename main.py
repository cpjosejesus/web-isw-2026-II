"""Biblioteca — CRUD completo con manejo de errores.

Las cuatro operaciones terminan igual: db.session.commit(), es decir un
COMMIT por el puerto 5432. Lo unico que cambia es el verbo HTTP y el SQL
que el ORM genera detras.
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
# Necesaria para firmar la sesion, que es donde viajan los mensajes flash.
app.secret_key = os.environ.get('SECRET_KEY', 'clave-de-desarrollo')

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

    # joinedload trae el autor en la misma consulta. Sin esto, la plantilla
    # dispara una consulta por cada libro al leer l.autor.nombre: el N+1.
    consulta = consulta.options(db.joinedload(Libro.autor))

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
            titulo=request.form['titulo'],          # KeyError → 400 si falta
            anio=request.form.get('anio') or None,  # seguro, con default
            autor_id=request.form['autor_id'],
            # un checkbox sin marcar no se envia: por eso 'in request.form'
            disponible='disponible' in request.form,
        )
        db.session.add(libro)
        db.session.commit()
        flash('Libro creado.', 'exito')
    except Exception:
        db.session.rollback()
        flash('No se pudo crear el libro.', 'error')

    # Post/Redirect/Get: nunca render_template como respuesta a un POST.
    return redirect(url_for('listar_libros'))


@app.route('/libros/<int:libro_id>/editar', methods=['GET', 'POST'])
def editar_libro(libro_id):
    """GET  →  el mismo formulario, ya cargado.
       POST →  actualiza el libro y redirige a su ficha."""
    libro = Libro.query.get_or_404(libro_id)

    if request.method == 'GET':
        return render_template('libros/formulario.html', libro=libro,
                               autores=Autor.query.order_by(Autor.nombre).all())

    try:
        # No hay db.session.add(): el objeto vino de una consulta, asi que
        # la sesion ya lo vigila y detecta el cambio sola.
        libro.titulo = request.form['titulo']
        libro.anio = request.form.get('anio') or None
        libro.autor_id = request.form['autor_id']
        libro.disponible = 'disponible' in request.form
        db.session.commit()
        flash('Cambios guardados.', 'exito')
    except Exception:
        db.session.rollback()
        flash('No se pudieron guardar los cambios.', 'error')

    return redirect(url_for('detalle_libro', libro_id=libro.id))


@app.route('/libros/<int:libro_id>/eliminar', methods=['POST'])
def eliminar_libro(libro_id):
    """POST  →  borra el libro. Nunca GET: un rastreador lo visitaria solo."""
    libro = Libro.query.get_or_404(libro_id)

    try:
        db.session.delete(libro)
        db.session.commit()
        flash('Libro eliminado.', 'exito')
    except Exception:
        db.session.rollback()
        flash('No se pudo eliminar el libro.', 'error')

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


@app.errorhandler(404)
def no_encontrado(error):
    # El segundo valor es el codigo de estado. Sin el responderias 200 OK
    # con una pagina que dice "no encontrado".
    return render_template('errores/404.html'), 404


@app.errorhandler(500)
def error_servidor(error):
    db.session.rollback()          # deja la sesion limpia
    return render_template('errores/500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
