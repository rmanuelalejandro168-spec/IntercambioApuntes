from sqlalchemy import Column, Integer, ForeignKey
from backend.database import Base


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Integer, nullable=False)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    autor_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    material_id = Column(
        Integer,
        ForeignKey("materiales.id"),
        nullable=False
    )