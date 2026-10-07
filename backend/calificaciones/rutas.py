from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.calificaciones.modelos import Calificacion
from backend.usuarios.modelos import Usuario
from backend.materiales.modelos import Material


router = APIRouter(
    prefix="/calificaciones",
    tags=["Calificaciones"]
)


class CalificacionCrear(BaseModel):
    valor: int
    usuario_id: int
    autor_id: int
    material_id: int


def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def crear_calificacion(
    calificacion: CalificacionCrear,
    db: Session = Depends(obtener_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == calificacion.usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="El usuario que califica no existe"
        )

    material = db.query(Material).filter(
        Material.id == calificacion.material_id
    ).first()

    if not material:
        raise HTTPException(
            status_code=404,
            detail="El material no existe"
        )

    if calificacion.usuario_id == calificacion.autor_id:
        raise HTTPException(
            status_code=400,
            detail="Un usuario no puede calificarse a sí mismo"
        )

    calificacion_existente = db.query(Calificacion).filter(
    Calificacion.usuario_id == calificacion.usuario_id,
    Calificacion.material_id == calificacion.material_id
).first()

    if calificacion_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya calificaste este material"
    )

    if calificacion.valor < 1 or calificacion.valor > 5:
        raise HTTPException(
            status_code=400,
            detail="La calificación debe estar entre 1 y 5"
        )

    nueva_calificacion = Calificacion(
        valor=calificacion.valor,
        usuario_id=calificacion.usuario_id,
        autor_id=calificacion.autor_id,
        material_id=calificacion.material_id
    )

    db.add(nueva_calificacion)
    db.commit()
    db.refresh(nueva_calificacion)

    return {
        "mensaje": "Calificación creada correctamente",
        "calificacion": nueva_calificacion
    }

@router.get("/material/{material_id}")
def obtener_calificacion_material(
    material_id: int,
    db: Session = Depends(obtener_db)
):
    material = db.query(Material).filter(
        Material.id == material_id
    ).first()

    if not material:
        raise HTTPException(
            status_code=404,
            detail="El material no existe"
        )

    calificaciones = db.query(Calificacion).filter(
        Calificacion.material_id == material_id
    ).all()

    if not calificaciones:
        return {
            "material_id": material_id,
            "promedio": 0,
            "total_calificaciones": 0
        }

    promedio = sum(
        calificacion.valor
        for calificacion in calificaciones
    ) / len(calificaciones)

    return {
        "material_id": material_id,
        "promedio": round(promedio, 1),
        "total_calificaciones": len(calificaciones)
    }