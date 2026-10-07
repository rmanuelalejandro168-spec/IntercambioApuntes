class Reporte:
    def __init__(self, motivo, usuario_id, material_id):
        if not motivo:
            raise ValueError("El motivo del reporte es obligatorio")

        if usuario_id is None:
            raise ValueError("El reporte debe tener un usuario")

        if material_id is None:
            raise ValueError("El reporte debe tener un material")

        self.motivo = motivo
        self.usuario_id = usuario_id
        self.material_id = material_id