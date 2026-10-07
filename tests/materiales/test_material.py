import pytest
from src.materiales.material import Material
from src.usuarios.usuario import Usuario


def test_crear_material():
    usuario = Usuario("Juan", "juan@email.com")
    material = Material("Guía de Matemáticas", "guia.pdf", usuario)

    assert material.titulo == "Guía de Matemáticas"
    assert material.archivo == "guia.pdf"


def test_material_debe_tener_titulo():
    usuario = Usuario("Juan", "juan@email.com")
    material = Material("Guía de Matemáticas", "guia.pdf", usuario)

    assert material.titulo != ""


def test_material_no_puede_crearse_sin_titulo():
    usuario = Usuario("Juan", "juan@email.com")

    with pytest.raises(ValueError):
        Material("", "guia.pdf", usuario)


def test_material_debe_tener_autor():
    usuario = Usuario("Juan", "juan@email.com")
    material = Material("Guía de Matemáticas", "guia.pdf", usuario)

    assert material.autor == usuario

def test_usuario_no_registrado_no_puede_subir_material():
    usuario = Usuario("Pedro", "pedro@email.com")
    usuario.registrado = False

    with pytest.raises(ValueError):
        Material("Guía de Física", "fisica.pdf", usuario)

def test_material_acepta_archivo_pdf():
    usuario = Usuario("Juan", "juan@email.com")
    material = Material("Guía de Matemáticas", "guia.pdf", usuario)

    assert material.archivo.endswith(".pdf")

def test_material_no_acepta_archivo_invalido():
    usuario = Usuario("Juan", "juan@email.com")

    try:
        Material("Apuntes", "archivo.exe", usuario)
        assert False
    except ValueError:
        assert True
