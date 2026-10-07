from sqlalchemy import Column, Integer, Text, ForeignKey

from backend.database import Base


class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, index=True)

    motivo = Column(Text, nullable=False)

    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    material_id = Column(
        Integer,
        ForeignKey("materiales.id"),
        nullable=False
    )