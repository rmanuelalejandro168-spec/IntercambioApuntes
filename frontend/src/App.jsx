import { useEffect, useState } from "react"
import { Routes, Route, useNavigate, Link } from "react-router-dom"
import "./App.css"

function App() {
  const navigate = useNavigate() // Hook para cambiar de página
  
  // Estados de datos
  const [materiales, setMateriales] = useState([])
  const [usuarioActual, setUsuarioActual] = useState(null)
  const [usuarioPerfil, setUsuarioPerfil] = useState(null)
  const [datosPerfil, setDatosPerfil] = useState(null)
  
  const [login, setLogin] = useState({ email: "", password: "" })
  const [registro, setRegistro] = useState({ nombre: "", email: "", password: "" })
  const [materia, setMateria] = useState("")
  const [materias, setMaterias] = useState([])
  const [materialSeleccionado, setMaterialSeleccionado] = useState(null)
  const [calificacion, setCalificacion] = useState({})
  const [promedios, setPromedios] = useState({})
  const [formulario, setFormulario] = useState({ titulo: "", materia: "", descripcion: "", archivo: "", autor_id: "" })

  const manejarCambioLogin = (evento) => {
    setLogin({ ...login, [evento.target.name]: evento.target.value })
  }

  const manejarCambioRegistro = (evento) => {
    setRegistro({ ...registro, [evento.target.name]: evento.target.value })
  }

  const manejarCambio = (evento) => {
    setFormulario({ ...formulario, [evento.target.name]: evento.target.value })
  }

  const obtenerPerfil = () => {
    if (!usuarioPerfil) return
    fetch(`http://127.0.0.1:8000/usuarios/${usuarioPerfil}`)
      .then((respuesta) => respuesta.json())
      .then((datos) => setDatosPerfil(datos))
      .catch((error) => console.error("Error al obtener perfil:", error))
  }

  useEffect(() => {
    obtenerPerfil()
  }, [usuarioPerfil])

  const iniciarSesion = () => {
    fetch("http://127.0.0.1:8000/usuarios/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(login)
    })
      .then((respuesta) => {
        if (!respuesta.ok) return respuesta.json().then((datos) => { throw new Error(datos.detail || "Error al iniciar sesión") })
        return respuesta.json()
      })
      .then((datos) => {
        setUsuarioActual(datos.usuario)
        setLogin({ email: "", password: "" })
        navigate("/") // <-- Redirige al inicio tras iniciar sesión
      })
      .catch((error) => alert(error.message))
  }

  const registrarUsuario = () => {
    fetch("http://127.0.0.1:8000/usuarios/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(registro)
    })
      .then((respuesta) => {
        if (!respuesta.ok) return respuesta.json().then((datos) => { throw new Error(datos.detail || "Error al crear la cuenta") })
        return respuesta.json()
      })
      .then((datos) => {
        alert(datos.mensaje)
        setRegistro({ nombre: "", email: "", password: "" })
        navigate("/login") // <-- Redirige al login tras registrarse
      })
      .catch((error) => alert(error.message))
  }

  useEffect(() => {
    fetch("http://127.0.0.1:8000/materias/")
      .then((respuesta) => respuesta.json())
      .then((datos) => setMaterias(datos.materias))
      .catch((error) => console.error("Error al obtener materias:", error))
  }, [])

  const cargarMateriales = () => {
    let url = "http://127.0.0.1:8000/materiales/"
    if (materia) url += `?materia=${encodeURIComponent(materia)}`
    fetch(url)
      .then((respuesta) => respuesta.json())
      .then((datos) => setMateriales(datos.materiales))
      .catch((error) => console.error("Error al obtener materiales:", error))
  }

  useEffect(() => {
    cargarMateriales()
  }, [materia])

  useEffect(() => {
    materiales.forEach((material) => {
      fetch(`http://127.0.0.1:8000/calificaciones/material/${material.id}`)
        .then((respuesta) => respuesta.json())
        .then((datos) => setPromedios((anteriores) => ({ ...anteriores, [material.id]: datos })))
        .catch((error) => console.error("Error al obtener calificación:", error))
    })
  }, [materiales])

  return (
    <div className="app">
      {/* El encabezado se queda fuera de <Routes> para que siempre sea visible */}
      <header className="encabezado">
        <div>
          <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            <h1>IntercambioApuntes</h1>
          </Link>
          <p>Comparte y encuentra material de estudio universitario.</p>
        </div>

        <button
          onClick={() => {
            if (usuarioActual) {
              setUsuarioActual(null)
            } else {
              navigate("/login") // <-- Navega a la pantalla de login
            }
          }}
        >
          {usuarioActual ? "Cerrar sesión" : "Iniciar sesión"}
        </button>
      </header>

      <main className="contenido">
        {/* Aquí definimos qué contenido se muestra en qué URL */}
        <Routes>
          
          {/* PANTALLA PRINCIPAL: Lista de materiales */}
          <Route path="/" element={
            <>
              <div className="titulo-seccion">
                <h2>Materiales disponibles</h2>
                <button onClick={() => {
                  if(!usuarioActual) {
                    alert("Debes iniciar sesión para subir material")
                    navigate("/login")
                  } else {
                    navigate("/subir")
                  }
                }}>
                  Subir material
                </button>
              </div>

              <div className="filtros">
                <label htmlFor="materia">Filtrar por materia:</label>
                <input
                  type="text"
                  id="materia"
                  value={materia}
                  onChange={(evento) => setMateria(evento.target.value)}
                  placeholder="Escribe una materia..."
                />
              </div>

              <div className="materiales">
                {materiales.length === 0 ? (
                  <p>No hay materiales para esta materia.</p>
                ) : (
                  materiales.map((material) => (
                    <div className="tarjeta" key={material.id}>
                      <h3>{material.titulo}</h3>
                      <p className="materia">{material.materia}</p>
                      
                      {/* Al hacer clic en el autor, guardamos el ID y navegamos a /perfil */}
                      <p className="autor" onClick={() => {
                          setUsuarioPerfil(material.autor_id)
                          navigate("/perfil")
                        }}
                        style={{ cursor: 'pointer' }}
                      >
                        👤 Compartido por <strong>{material.autor_nombre}</strong>
                      </p>

                      <p>{material.descripcion}</p>

                      <div className="promedio">
                        {promedios[material.id]?.total_calificaciones > 0 ? (
                          <p>
                            ⭐ {promedios[material.id].promedio} / 5 — {promedios[material.id].total_calificaciones}{" "}
                            {promedios[material.id].total_calificaciones === 1 ? "calificación" : "calificaciones"}
                          </p>
                        ) : (
                          <p>⭐ Sin calificaciones</p>
                        )}
                      </div>

                      <button className="boton-ver" onClick={() => setMaterialSeleccionado(material)}>
                        Ver detalles
                      </button>

                      <div className="calificacion">
                        <p>Calificar material:</p>
                        <select
                          value={calificacion[material.id] || ""}
                          onChange={(evento) => setCalificacion({ ...calificacion, [material.id]: evento.target.value })}
                        >
                          <option value="">Selecciona</option>
                          <option value="1">⭐ 1</option>
                          <option value="2">⭐⭐ 2</option>
                          <option value="3">⭐⭐⭐ 3</option>
                          <option value="4">⭐⭐⭐⭐ 4</option>
                          <option value="5">⭐⭐⭐⭐⭐ 5</option>
                        </select>
                        <button
                          onClick={() => {
                            if (!usuarioActual) {
                              alert("Debes iniciar sesión para calificar")
                              navigate("/login")
                              return
                            }
                            if (!calificacion[material.id]) {
                              alert("Selecciona una calificación")
                              return
                            }
                            fetch("http://127.0.0.1:8000/calificaciones/", {
                              method: "POST",
                              headers: { "Content-Type": "application/json" },
                              body: JSON.stringify({
                                valor: Number(calificacion[material.id]),
                                usuario_id: usuarioActual.id,
                                autor_id: material.autor_id,
                                material_id: material.id
                              })
                            })
                              .then((respuesta) => respuesta.json())
                              .then((datos) => alert(datos.mensaje || datos.detail))
                              .catch((error) => alert("No se pudo guardar la calificación"))
                          }}
                        >
                          Calificar
                        </button>
                      </div>

                      {material.archivo && (
                        <button
                          className="boton-pdf"
                          onClick={() => window.open(`http://127.0.0.1:8000/materiales/${material.id}/archivo`, "_blank")}
                        >
                          Abrir PDF
                        </button>
                      )}

                      {materialSeleccionado?.id === material.id && (
                        <div className="detalle">
                          <hr />
                          <p><strong>Archivo:</strong> {material.archivo || "No especificado"}</p>
                          <p><strong>Autor:</strong> {material.autor_nombre}</p>
                          <button onClick={() => setMaterialSeleccionado(null)}>Cerrar</button>
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </>
          } />

          {/* PANTALLA LOGIN */}
          <Route path="/login" element={
            <div className="formulario">
              <h2>Iniciar sesión</h2>
              <input type="email" name="email" placeholder="Correo electrónico" value={login.email} onChange={manejarCambioLogin} />
              <input type="password" name="password" placeholder="Contraseña" value={login.password} onChange={manejarCambioLogin} />
              
              <button onClick={iniciarSesion}>Iniciar sesión</button>
              <button onClick={() => navigate("/")}>Cancelar</button>
              <button onClick={() => navigate("/registro")}>Crear una cuenta</button>
            </div>
          } />

          {/* PANTALLA REGISTRO */}
          <Route path="/registro" element={
            <div className="formulario">
              <h2>Crear cuenta</h2>
              <input type="text" name="nombre" placeholder="Nombre completo" value={registro.nombre} onChange={manejarCambioRegistro} />
              <input type="email" name="email" placeholder="Correo electrónico" value={registro.email} onChange={manejarCambioRegistro} />
              <input type="password" name="password" placeholder="Contraseña" value={registro.password} onChange={manejarCambioRegistro} />
              
              <button onClick={registrarUsuario}>Crear cuenta</button>
              <button onClick={() => navigate("/login")}>Ya tengo una cuenta</button>
            </div>
          } />

          {/* PANTALLA SUBIR MATERIAL */}
          <Route path="/subir" element={
            <div className="formulario">
              <h2>Subir material</h2>
              <input type="text" name="titulo" placeholder="Título del material" value={formulario.titulo} onChange={manejarCambio} />
              <input type="text" name="materia" placeholder="Materia" value={formulario.materia} onChange={manejarCambio} />
              <textarea name="descripcion" placeholder="Descripción" value={formulario.descripcion} onChange={manejarCambio} />
              
              <input type="file" name="archivo" accept=".pdf" onChange={(evento) => setFormulario({ ...formulario, archivo: evento.target.files[0] })} />

              <button
                onClick={() => {
                  const datos = new FormData()
                  datos.append("titulo", formulario.titulo)
                  datos.append("materia", formulario.materia)
                  datos.append("descripcion", formulario.descripcion)
                  datos.append("autor_id", usuarioActual.id)
                  datos.append("archivo", formulario.archivo)

                  fetch("http://127.0.0.1:8000/materiales/", {
                    method: "POST",
                    body: datos
                  })
                    .then((respuesta) => respuesta.json())
                    .then((datos) => {
                      cargarMateriales()
                      setFormulario({ titulo: "", materia: "", descripcion: "", archivo: "", autor_id: "" })
                      navigate("/") // Vuelve al inicio tras guardar
                    })
                    .catch((error) => console.error("ERROR AL SUBIR:", error))
                }}
              >
                Guardar material
              </button>
              <button onClick={() => navigate("/")}>Cancelar</button>
            </div>
          } />

          {/* PANTALLA PERFIL */}
          <Route path="/perfil" element={
            datosPerfil ? (
              <div className="perfil">
                <button
                  className="perfil-cerrar"
                  onClick={() => {
                    setUsuarioPerfil(null)
                    setDatosPerfil(null)
                    navigate(-1) // Vuelve a la página anterior en el historial
                  }}
                >
                  ← Volver
                </button>
                <div className="perfil-contenido">
                  <div className="perfil-avatar">👤</div>
                  <h2>{datosPerfil.nombre}</h2>
                  <p className="perfil-correo">{datosPerfil.email}</p>
                  <p className="perfil-estado">
                    {datosPerfil.registrado ? "Usuario registrado" : "Usuario no registrado"}
                  </p>
                </div>
              </div>
            ) : (
              <p>Cargando perfil...</p>
            )
          } />

        </Routes>
      </main>
    </div>
  )
}

export default App