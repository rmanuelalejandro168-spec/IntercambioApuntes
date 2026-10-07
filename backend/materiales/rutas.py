import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.materiales.modelos import Material
from backend.usuarios.modelos import Usuario
from backend.materias.modelos import Materia



router = APIRouter(
    prefix="/materiales",
    tags=["Materiales"]
)


class MaterialCrear(BaseModel):
    titulo: str
    materia: str
    descripcion: str
    archivo: str = ""
    autor_id: int


def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def obtener_materiales(
    materia: str = None,
    db: Session = Depends(obtener_db)
):
    consulta = db.query(Material)

    if materia:
     consulta = consulta.filter(
        Material.materia.ilike(f"%{materia}%")
    )

    materiales = consulta.all()

    resultado = []
    for material in materiales:
        usuario = db.query(Usuario).filter(
            Usuario.id == material.autor_id
            ).first()

        resultado.append({
            "id": material.id,
            "titulo": material.titulo,
            "materia": material.materia,
            "descripcion": material.descripcion,
            "archivo": material.archivo,
            "autor_id": material.autor_id,
            "autor_nombre": usuario.nombre if usuario else "Usuario desconocido"
            })


    return {
        "materiales": resultado
    }


@router.post("/")
def crear_material(
    titulo: str = Form(...),
    materia: str = Form(...),
    descripcion: str = Form(...),
    autor_id: int = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(obtener_db)
):
    if not materia.strip():
     raise HTTPException(
        status_code=400,
        detail="La materia es obligatoria"
    )
    
    usuario = db.query(Usuario).filter(
        Usuario.id == autor_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="El usuario autor no existe"
        )

    if not usuario.registrado:
        raise HTTPException(
            status_code=403,
            detail="El usuario no está registrado"
        )
    materia_existente = db.query(Materia).filter(
         Materia.nombre.ilike(materia)
    ).first()

    if not materia_existente:
        nueva_materia = Materia(
            nombre=materia
             )

        db.add(nueva_materia)
        db.commit()
        db.refresh(nueva_materia)

    if not archivo.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser PDF"
        )

    carpeta_uploads = "backend/uploads"

    os.makedirs(carpeta_uploads, exist_ok=True)

    ruta_archivo = os.path.join(
        carpeta_uploads,
        archivo.filename
    )

    with open(ruta_archivo, "wb") as archivo_destino:
        archivo_destino.write(archivo.file.read())

    nuevo_material = Material(
        titulo=titulo,
        materia=materia,
        descripcion=descripcion,
        archivo=archivo.filename,
        autor_id=autor_id
    )

    db.add(nuevo_material)
    db.commit()
    db.refresh(nuevo_material)

    return {
        "mensaje": "Material creado correctamente",
        "material": nuevo_material
    }


@router.get("/{material_id}/archivo")
def descargar_archivo(
    material_id: int,
    db: Session = Depends(obtener_db)
):
    material = db.query(Material).filter(
        Material.id == material_id
    ).first()

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Material no encontrado"
        )

    ruta_archivo = os.path.join(
        "backend/uploads",
        material.archivo
    )

    if not os.path.exists(ruta_archivo):
        raise HTTPException(
            status_code=404,
            detail="El archivo no existe"
        )

    return FileResponse(
        ruta_archivo,
        media_type="application/pdf",
        filename=material.archivo
    )