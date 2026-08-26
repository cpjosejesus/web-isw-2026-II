"""Biblioteca — todavia responde JSON.

En este paso solo cambia el dominio: Person deja lugar a Autor y Libro,
con una relacion uno-a-muchos. Las rutas siguen hablando JSON; en el
paso siguiente empiezan a devolver HTML.
"""
import os

from flask import Flask, jsonify, abort, request

from models import db, Autor, Libro

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql+psycopg://app:123qwe@localhost:5433/store'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/autores', methods=['GET'])
def listar_autores():
    """GET /autores  →  todos los autores con su cantidad de libros."""
    autores = Autor.query.order_by(Autor.nombre).all()
    return jsonify({
        'success': True,
        'total': len(autores),
        'autores': [a.format() for a in autores],
    })


@app.route('/libros', methods=['GET'])
def listar_libros():
    """GET /libros  →  todos los libros. Acepta ?autor=... para filtrar."""
    consulta = Libro.query

    autor = request.args.get('autor')
    if autor:
        consulta = consulta.join(Autor).filter(
            Autor.nombre.ilike(f'%{autor}%'))

    libros = consulta.order_by(Libro.titulo).all()

    return jsonify({
        'success': True,
        'total': len(libros),
        'libros': [l.format() for l in libros],
    })


@app.route('/libros/<int:libro_id>', methods=['GET'])
def obtener_libro(libro_id):
    """GET /libros/3  →  un solo libro, o 404."""
    libro = Libro.query.get(libro_id)

    if libro is None:
        abort(404)

    return jsonify({'success': True, 'libro': libro.format()})


@app.route('/', methods=['GET'])
def salud():
    """GET /  →  comprobacion rapida de que la conexion funciona."""
    return jsonify({
        'status': 'ok',
        'autores': Autor.query.count(),
        'libros': Libro.query.count(),
    })


@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({'success': False, 'error': 404,
                    'mensaje': 'recurso no encontrado'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
