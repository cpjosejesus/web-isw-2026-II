"""Crea la tabla `persons` y la puebla con ~50 registros de ejemplo.

Uso:
    uv run seed.py            # crea la tabla y la puebla si esta vacia
    uv run seed.py --reset    # borra las filas existentes y vuelve a poblar
"""
import sys

from main import app, db, Person

NOMBRES = [
    'Ana', 'Luis', 'Maria', 'Carlos', 'Sofia', 'Miguel', 'Lucia', 'Javier',
    'Elena', 'Diego', 'Carmen', 'Andres', 'Paula', 'Ricardo', 'Valeria',
    'Fernando', 'Isabel', 'Alejandro', 'Natalia', 'Sergio', 'Patricia',
    'Rodrigo', 'Gabriela', 'Tomas', 'Daniela',
]

APELLIDOS = [
    'Garcia', 'Rodriguez', 'Martinez', 'Lopez', 'Perez', 'Gonzalez',
    'Sanchez', 'Ramirez', 'Torres', 'Flores', 'Rivera', 'Gomez',
    'Diaz', 'Vargas', 'Castillo', 'Morales', 'Ortiz', 'Silva',
    'Rojas', 'Medina',
]


def generar_personas(cantidad=50):
    """Genera `cantidad` personas con nombre unico, edad y correo."""
    personas = []
    for i in range(cantidad):
        nombre = NOMBRES[i % len(NOMBRES)]
        apellido = APELLIDOS[(i * 7) % len(APELLIDOS)]
        nombre_completo = f'{nombre} {apellido}'

        # El nombre es UNIQUE en la tabla: si se repite, agregamos un sufijo.
        if any(p.name == nombre_completo for p in personas):
            nombre_completo = f'{nombre_completo} {i}'

        correo = f'{nombre.lower()}.{apellido.lower()}{i}@example.com'
        edad = 18 + (i * 3) % 50

        personas.append(Person(name=nombre_completo, age=edad, email=correo))
    return personas


def main():
    reset = '--reset' in sys.argv

    with app.app_context():
        db.create_all()
        print('Tabla `persons` lista.')

        if reset:
            borradas = Person.query.delete()
            db.session.commit()
            print(f'Se borraron {borradas} registros previos.')

        existentes = Person.query.count()
        if existentes and not reset:
            print(f'La tabla ya tiene {existentes} registros; '
                  f'usa --reset para regenerarlos.')
            return

        db.session.add_all(generar_personas(50))
        db.session.commit()
        print(f'Insertados {Person.query.count()} registros en `persons`.')


if __name__ == '__main__':
    main()
