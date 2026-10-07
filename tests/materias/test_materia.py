from src.materias.materia import Materia


def test_crear_materia():
    materia = Materia("Matemáticas")

    assert materia.nombre == "Matemáticas"