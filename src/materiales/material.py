class Material:
    def __init__(self, titulo, archivo, autor):
        if not titulo:
            raise ValueError("El título es obligatorio")

        if not autor.registrado:
            raise ValueError("El usuario debe estar registrado")

        extensiones_validas = (".pdf", ".docx", ".pptx")

        if not archivo.lower().endswith(extensiones_validas):
            raise ValueError("El formato del archivo no es válido")

        self.titulo = titulo
        self.archivo = archivo
        self.autor = autor