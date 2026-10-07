from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.comentarios.modelos import Comentario
from backend.usuarios.modelos import Usuario
from backend.materiales.modelos import Material


router = APIRouter(
    prefix="/comentarios",
    tags=["Comentarios"]
)


class ComentarioCrear(BaseModel):
    texto: str
    usuario_id: int
    material_id: int


def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def obtener_comentarios(
    db: Session = Depends(obtener_db)
):
    comentarios = db.query(Comentario).all()

    return {
        "comentarios": comentarios
    }


@router.post("/")
def crear_comentario(
    comentario: ComentarioCrear,
    db: Session = Depends(obtener_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == comentario.usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="El usuario no existe"
        )

    material = db.query(Material).filter(
        Material.id == comentario.material_id
    ).first()

    if not material:
        raise HTTPException(
            status_code=404,
            detail="El material no existe"
        )

    if not comentario.texto:
        raise HTTPException(
            status_code=400,
            detail="El comentario no puede estar vacío"
        )

    nuevo_comentario = Comentario(
        texto=comentario.texto,
        usuario_id=comentario.usuario_id,
        material_id=comentario.material_id
    )

    db.add(nuevo_comentario)
    db.commit()
    db.refresh(nuevo_comentario)

    return {
        "mensaje": "Comentario creado correctamente",
        "comentario": nuevo_comentario
    }