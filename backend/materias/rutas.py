from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.materias.modelos import Materia


router = APIRouter(
    prefix="/materias",
    tags=["Materias"]
)


def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def obtener_materias(
    db: Session = Depends(obtener_db)
):
    materias = db.query(Materia).order_by(Materia.nombre).all()

    return {
        "materias": materias
    }


@router.post("/")
def crear_materia(
    nombre: str,
    db: Session = Depends(obtener_db)
):
    materia_existente = db.query(Materia).filter(
        Materia.nombre == nombre
    ).first()

    if materia_existente:
        return {
            "mensaje": "La materia ya existe",
            "materia": materia_existente
        }

    nueva_materia = Materia(
        nombre=nombre
    )

    db.add(nueva_materia)
    db.commit()
    db.refresh(nueva_materia)

    return {
        "mensaje": "Materia creada correctamente",
        "materia": nueva_materia
    }