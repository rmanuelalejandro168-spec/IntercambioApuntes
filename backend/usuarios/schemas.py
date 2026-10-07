from pydantic import BaseModel


class UsuarioCrear(BaseModel):
    nombre: str
    email: str
    password: str

class UsuarioLogin(BaseModel):
    email: str
    password: str