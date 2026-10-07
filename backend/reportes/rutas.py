from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.reportes.modelos import Reporte
from backend.usuarios.modelos import Usuario
from backend.materiales.modelos import Material


router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)


class ReporteCrear(BaseModel):
    motivo: str
    usuario_id: int
    material_id: int


def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def obtener_reportes(
    db: Session = Depends(obtener_db)
):
    reportes = db.query(Reporte).all()

    return {
        "reportes": reportes
    }


@router.post("/")
def crear_reporte(
    reporte: ReporteCrear,
    db: Session = Depends(obtener_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == reporte.usuario_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="El usuario no existe"
        )

    material = db.query(Material).filter(
        Material.id == reporte.material_id
    ).first()

    if not material:
        raise HTTPException(
            status_code=404,
            detail="El material no existe"
        )

    if not reporte.motivo:
        raise HTTPException(
            status_code=400,
            detail="El motivo del reporte es obligatorio"
        )

    nuevo_reporte = Reporte(
        motivo=reporte.motivo,
        usuario_id=reporte.usuario_id,
        material_id=reporte.material_id
    )

    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)

    return {
        "mensaje": "Reporte creado correctamente",
        "reporte": nuevo_reporte
    }