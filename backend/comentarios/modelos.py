from sqlalchemy import Column, Integer, Text, ForeignKey

from backend.database import Base


class Comentario(Base):
    __tablename__ = "comentarios"

    id = Column(Integer, primary_key=True, index=True)

    texto = Column(Text, nullable=False)

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