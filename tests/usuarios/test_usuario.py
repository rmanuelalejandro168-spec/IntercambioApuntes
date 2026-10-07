from src.usuarios.usuario import Usuario


def test_crear_usuario():
    usuario = Usuario("Juan", "juan@email.com")

    assert usuario.nombre == "Juan"
    assert usuario.email == "juan@email.com"


def test_usuario_debe_tener_nombre():
    usuario = Usuario("Juan", "juan@email.com")

    assert usuario.nombre != ""


def test_usuario_debe_tener_email():
    usuario = Usuario("Juan", "juan@email.com")

    assert usuario.email != ""

def test_usuario_registrado():
    usuario = Usuario("Juan", "juan@email.com")

    assert usuario.registrado is True 

def test_usuario_no_puede_crearse_sin_nombre():
    try:
        Usuario("", "juan@email.com")
        assert False
    except ValueError:
        assert True

def test_usuario_no_puede_crearse_sin_email():
    try:
        Usuario("Juan", "")
        assert False
    except ValueError:
        assert True

