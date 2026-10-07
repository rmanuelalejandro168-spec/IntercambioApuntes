Característica: Gestión de materiales de estudio

  Escenario: Un usuario registrado sube un material válido
    Dado que existe un usuario registrado
    Cuando intenta subir una guía en PDF
    Entonces el sistema acepta el material

  Escenario: Un usuario no registrado intenta subir material
    Dado que existe un usuario no registrado
    Cuando intenta subir un material
    Entonces el sistema rechaza el material

  Escenario: Un usuario registrado intenta subir un archivo inválido
    Dado que existe un usuario registrado
    Cuando intenta subir un archivo EXE
    Entonces el sistema rechaza el material

  Escenario: Un material no puede tener título vacío
    Dado que existe un usuario registrado
    Cuando intenta crear un material sin título
    Entonces el sistema rechaza el material