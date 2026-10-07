class Calificacion:
    def __init__(
        self,
        valor,
        usuario_id=None,
        autor_id=None,
        material_id=None
    ):
        if valor < 1 or valor > 5:
            raise ValueError("La calificación debe estar entre 1 y 5")

        if usuario_id is not None and autor_id is not None:
            if usuario_id == autor_id:
                raise ValueError(
                    "Un usuario no puede calificarse a sí mismo"
                )

        self.valor = valor
        self.usuario_id = usuario_id
        self.autor_id = autor_id
        self.material_id = material_id