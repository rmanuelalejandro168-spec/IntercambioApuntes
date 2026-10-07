from sqlalchemy import Column, Integer, String, Text, ForeignKey
from backend.database import Base


class Material(Base):
    __tablename__ = "materiales"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    materia = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    archivo = Column(String(255), nullable=False, default="")
    autor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)