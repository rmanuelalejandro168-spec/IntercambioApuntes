class Usuario:
    def __init__(self, nombre, email):
        if not nombre:
            raise ValueError("El nombre es obligatorio")

        if not email:
            raise ValueError("El email es obligatorio")

        self.nombre = nombre
        self.email = email
        self.registrado = True