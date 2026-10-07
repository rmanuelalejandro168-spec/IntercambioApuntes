import pytest

from src.comentarios.comentario import Comentario


def test_crear_comentario():
    comentario = Comentario(
        "Este material me ayudó mucho",
        2,
        1
    )

    assert comentario.texto == "Este material me ayudó mucho"
    assert comentario.usuario_id == 2
    assert comentario.material_id == 1

def test_comentario_no_puede_estar_vacio():
    usuario_id = 2
    material_id = 1

    with pytest.raises(ValueError):
        Comentario("", usuario_id, material_id)

def test_comentario_debe_tener_usuario():
    with pytest.raises(ValueError):
        Comentario("Buen material", None, 1)

def test_comentario_debe_tener_material():
    with pytest.raises(ValueError):
        Comentario("Buen material", 2, None)