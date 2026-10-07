class Comentario:
    def __init__(self, texto, usuario_id, material_id):
        if not texto:
            raise ValueError("El comentario es obligatorio")

        if usuario_id is None:
            raise ValueError("El comentario debe tener un usuario")

        if material_id is None:
            raise ValueError("El comentario debe tener un material")
            
        self.texto = texto
        self.usuario_id = usuario_id
        self.material_id = material_id