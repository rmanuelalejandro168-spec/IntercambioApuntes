import pytest

from src.reportes.reporte import Reporte


def test_crear_reporte():
    reporte = Reporte(
        "Contenido incorrecto",
        2,
        1
    )

    assert reporte.motivo == "Contenido incorrecto"
    assert reporte.usuario_id == 2
    assert reporte.material_id == 1

def test_reporte_debe_tener_usuario():
    with pytest.raises(ValueError):
        Reporte("Contenido incorrecto", None, 1)

def test_reporte_debe_tener_material():
    with pytest.raises(ValueError):
        Reporte("Contenido incorrecto", 2, None)