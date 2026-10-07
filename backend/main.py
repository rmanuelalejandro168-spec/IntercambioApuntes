from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.materiales import modelos as modelos_materiales
from backend.materiales.rutas import router as materiales_router
from backend.usuarios import modelos as modelos_usuarios
from backend.usuarios.rutas import router as usuarios_router
from backend.materias import modelos as modelos_materias
from backend.materias.rutas import router as materias_router
from backend.calificaciones import modelos as modelos_calificaciones
from backend.calificaciones.rutas import router as calificaciones_router
from backend.comentarios import modelos as modelos_comentarios
from backend.comentarios.rutas import router as comentarios_router
from backend.reportes import modelos as modelos_reportes
from backend.reportes.rutas import router as reportes_router



Base.metadata.create_all(bind=engine)


app = FastAPI(title="Intercambio de Apuntes")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de Intercambio de Apuntes funcionando"
    }


app.include_router(materiales_router)
app.include_router(usuarios_router)
app.include_router(calificaciones_router)
app.include_router(comentarios_router)
app.include_router(reportes_router)
app.include_router(materias_router)