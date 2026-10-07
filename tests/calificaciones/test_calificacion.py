import pytest

from src.calificaciones.calificacion import Calificacion


def test_crear_calificacion():
    calificacion = Calificacion(5)

    assert calificacion.valor == 5


def test_calificacion_debe_estar_entre_1_y_5():
    calificacion = Calificacion(4)

    assert 1 <= calificacion.valor <= 5


def test_calificacion_no_puede_ser_menor_que_1():
    with pytest.raises(ValueError):
        Calificacion(0)


def test_calificacion_no_puede_ser_mayor_que_5():
    with pytest.raises(ValueError):
        Calificacion(6)

def test_usuario_no_puede_calificarse_a_si_mismo():
    usuario_id = 1
    autor_id = 1

    with pytest.raises(ValueError):
        Calificacion(5, usuario_id, autor_id)

def test_calificacion_debe_tener_material():
    usuario_id = 2
    autor_id = 1
    material_id = 1

    calificacion = Calificacion(
        5,
        usuario_id,
        autor_id,
        material_id
    )

    assert calificacion.material_id == material_id