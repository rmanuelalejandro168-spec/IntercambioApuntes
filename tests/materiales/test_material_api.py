from fastapi.testclient import TestClient

from backend.main import app
from backend.database import SessionLocal
from backend.usuarios.modelos import Usuario


client = TestClient(app)


def test_no_se_puede_crear_material_con_autor_inexistente():
    respuesta = client.post(
        "/materiales/",
        json={
            "titulo": "Guía de Física",
            "materia": "Física",
            "descripcion": "Guía para el examen",
            "autor_id": 999
        }
    )

    assert respuesta.status_code == 404

def test_filtrar_materiales_por_materia():
    respuesta = client.get(
        "/materiales/?materia=Cálculo"
    )

    assert respuesta.status_code == 200

    datos = respuesta.json()

    for material in datos["materiales"]:
        assert material["materia"] == "Cálculo"

def test_usuario_no_registrado_no_puede_crear_material():
    db = SessionLocal()

    usuario = db.query(Usuario).filter(
        Usuario.id == 2
    ).first()

    usuario.registrado = False
    db.commit()

    try:
        respuesta = client.post(
            "/materiales/",
            json={
                "titulo": "Material de prueba",
                "materia": "Programación",
                "descripcion": "Material de prueba",
                "autor_id": 2
            }
        )

        assert respuesta.status_code == 403

    finally:
        usuario.registrado = True
        db.commit()
        db.close()

def test_material_api_no_acepta_archivo_invalido():
    respuesta = client.post(
        "/materiales/",
        json={
            "titulo": "Apuntes",
            "materia": "Programación",
            "descripcion": "Apuntes de programación",
            "archivo": "archivo.exe",
            "autor_id": 1
        }
    )

    assert respuesta.status_code == 400