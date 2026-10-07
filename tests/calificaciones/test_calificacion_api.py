from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_crear_calificacion():
    respuesta = client.post(
        "/calificaciones/",
        json={
            "valor": 5,
            "usuario_id": 2,
            "autor_id": 1,
            "material_id": 1
        }
    )

    assert respuesta.status_code == 200

def test_usuario_no_puede_calificarse_a_si_mismo():
    respuesta = client.post(
        "/calificaciones/",
        json={
            "valor": 5,
            "usuario_id": 1,
            "autor_id": 1,
            "material_id": 1
        }
    )

    assert respuesta.status_code == 400

def test_calificacion_api_no_acepta_valor_mayor_que_5():
    respuesta = client.post(
        "/calificaciones/",
        json={
            "valor": 6,
            "usuario_id": 2,
            "autor_id": 1,
            "material_id": 1
        }
    )

    assert respuesta.status_code == 400

def test_calificacion_api_no_acepta_valor_menor_que_1():
    respuesta = client.post(
        "/calificaciones/",
        json={
            "valor": 0,
            "usuario_id": 2,
            "autor_id": 1,
            "material_id": 1
        }
    )

    assert respuesta.status_code == 400

def test_calificacion_no_puede_usar_material_inexistente():
    respuesta = client.post(
        "/calificaciones/",
        json={
            "valor": 5,
            "usuario_id": 2,
            "autor_id": 1,
            "material_id": 999
        }
    )

    assert respuesta.status_code == 404