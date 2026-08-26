"""Crea las tablas `autores` y `libros` y las puebla con datos de ejemplo.

Uso:
    uv run seed.py            # crea las tablas y puebla si estan vacias
    uv run seed.py --reset    # borra lo existente y vuelve a poblar
"""
import sys

from main import app
from models import db, Autor, Libro

CATALOGO = [
    ('James Kurose', 'Estados Unidos', [
        ('Redes de computadoras', 2017, True),
        ('Computer Networking: A Top-Down Approach', 2020, True),
    ]),
    ('Andrew Tanenbaum', 'Paises Bajos', [
        ('Sistemas operativos modernos', 2009, True),
        ('Redes de computadoras', 2011, False),
        ('Organizacion de computadoras', 2013, True),
    ]),
    ('Robert Martin', 'Estados Unidos', [
        ('Clean Code', 2008, True),
        ('Clean Architecture', 2017, False),
    ]),
    ('Martin Fowler', 'Reino Unido', [
        ('Refactoring', 1999, True),
        ('Patterns of Enterprise Application Architecture', 2002, True),
    ]),
    ('Gabriel Garcia Marquez', 'Colombia', [
        ('Cien anios de soledad', 1967, True),
        ('El amor en los tiempos del colera', 1985, False),
    ]),
    ('Isabel Allende', 'Chile', [
        ('La casa de los espiritus', 1982, True),
    ]),
]


def poblar():
    """Inserta los autores con sus libros; la cascada guarda ambos."""
    for nombre, nacionalidad, libros in CATALOGO:
        autor = Autor(nombre=nombre, nacionalidad=nacionalidad)
        for titulo, anio, disponible in libros:
            autor.libros.append(
                Libro(titulo=titulo, anio=anio, disponible=disponible))
        db.session.add(autor)
    db.session.commit()


def main():
    reset = '--reset' in sys.argv

    with app.app_context():
        db.create_all()
        print('Tablas `autores` y `libros` listas.')

        if reset:
            # Borrar el autor arrastra sus libros por la cascada.
            for autor in Autor.query.all():
                db.session.delete(autor)
            db.session.commit()
            print('Se borraron los registros previos.')

        if Autor.query.count() and not reset:
            print(f'Ya hay {Autor.query.count()} autores; '
                  f'usa --reset para regenerarlos.')
            return

        poblar()
        print(f'Insertados {Autor.query.count()} autores y '
              f'{Libro.query.count()} libros.')


if __name__ == '__main__':
    main()
