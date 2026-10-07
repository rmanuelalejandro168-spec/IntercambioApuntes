from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.usuarios.modelos import Usuario
from backend.usuarios.schemas import UsuarioCrear, UsuarioLogin

import bcrypt


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def obtener_usuarios(db: Session = Depends(obtener_db)):
    usuarios = db.query(Usuario).all()

    return {
        "usuarios": usuarios
    }

@router.get("/{usuario_id}")
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(obtener_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "registrado": usuario.registrado
    }


@router.post("/")
def crear_usuario(
    usuario: UsuarioCrear,
    db: Session = Depends(obtener_db)
):
    password_hash = bcrypt.hashpw(
        usuario.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        password_hash=password_hash
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {
    "mensaje": "Usuario creado correctamente",
    "usuario": {
        "id": nuevo_usuario.id,
        "nombre": nuevo_usuario.nombre,
        "email": nuevo_usuario.email,
        "registrado": nuevo_usuario.registrado
    }
}

@router.post("/login")
def iniciar_sesion(
    usuario: UsuarioLogin,
    db: Session = Depends(obtener_db)
):
    usuario_db = db.query(Usuario).filter(
        Usuario.email == usuario.email
    ).first()

    if not usuario_db:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    if not usuario_db.password_hash:
        raise HTTPException(
            status_code=401,
            detail="Este usuario no tiene una contraseña registrada"
        )

    contraseña_correcta = bcrypt.checkpw(
        usuario.password.encode("utf-8"),
        usuario_db.password_hash.encode("utf-8")
    )

    if not contraseña_correcta:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    return {
        "mensaje": "Inicio de sesión correcto",
        "usuario": {
            "id": usuario_db.id,
            "nombre": usuario_db.nombre,
            "email": usuario_db.email,
            "registrado": usuario_db.registrado
        }
    }