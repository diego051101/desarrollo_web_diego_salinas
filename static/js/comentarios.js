// Comentarios de un avistamiento (Tarea 3): carga el listado y envía nuevos
// comentarios con fetch, sin recargar la página. La URL de la API sale del
// atributo action del formulario y los largos permitidos de sus atributos
// minlength/maxlength, que la plantilla toma de config.py, así el navegador
// y el servidor validan con exactamente las mismas reglas.
const formularioComentario = document.getElementById("formulario-comentario");
const listaComentarios = document.getElementById("lista-comentarios");
const estadoComentarios = document.getElementById("estado-comentarios");
const estadoEnvio = document.getElementById("estado-envio-comentario");
const botonEnviar = formularioComentario.querySelector('button[type="submit"]');

const CAMPOS = {
    nombre: { elemento: formularioComentario.elements.nombre, etiqueta: "El nombre" },
    texto: { elemento: formularioComentario.elements.texto, etiqueta: "El comentario" },
};

function crearItemComentario(comentario) {
    const autor = document.createElement("strong");
    autor.textContent = comentario.nombre;

    const fecha = document.createElement("time");
    fecha.dateTime = comentario.fecha_iso;
    fecha.textContent = comentario.fecha;

    const cabecera = document.createElement("p");
    cabecera.className = "cabecera-comentario";
    cabecera.append(autor, fecha);

    const texto = document.createElement("p");
    texto.className = "texto-comentario";
    texto.textContent = comentario.texto;

    const item = document.createElement("li");
    item.className = "item-comentario";
    item.append(cabecera, texto);
    return item;
}

function actualizarEstadoVacio() {
    estadoComentarios.textContent = listaComentarios.children.length === 0
        ? "Todavía no hay comentarios. ¡Sé la primera persona en comentar!"
        : "";
}

function cargarComentarios() {
    fetch(formularioComentario.action)
        .then(function (respuesta) {
            if (!respuesta.ok) throw new Error(respuesta.status);
            return respuesta.json();
        })
        .then(function (datos) {
            listaComentarios.replaceChildren(...datos.comentarios.map(crearItemComentario));
            actualizarEstadoVacio();
        })
        .catch(function () {
            estadoComentarios.textContent = "No fue posible cargar los comentarios. Recarga la página para intentarlo de nuevo.";
        });
}

// Caracteres de 4 bytes (emojis), que la base de datos en utf8 no admite.
const CARACTERES_DE_4_BYTES = /[\u{10000}-\u{10FFFF}]/u;

function validarComentario() {
    const errores = {};
    for (const [nombre, campo] of Object.entries(CAMPOS)) {
        const valor = campo.elemento.value.trim();
        const { minLength, maxLength } = campo.elemento;
        if (valor.length < minLength || valor.length > maxLength) {
            errores[nombre] = `${campo.etiqueta} debe tener entre ${minLength} y ${maxLength} caracteres.`;
        } else if (CARACTERES_DE_4_BYTES.test(valor)) {
            errores[nombre] = `${campo.etiqueta} no puede contener emojis.`;
        }
    }
    return errores;
}

function mostrarErrores(errores) {
    for (const [nombre, campo] of Object.entries(CAMPOS)) {
        const mensaje = errores[nombre] || "";
        campo.elemento.closest(".grupo-formulario").classList.toggle("con-error", mensaje !== "");
        campo.elemento.setAttribute("aria-invalid", mensaje !== "");
        document.getElementById(`error-${nombre}`).textContent = mensaje;
    }
    const primerCampoConError = Object.keys(errores)[0];
    if (primerCampoConError) CAMPOS[primerCampoConError].elemento.focus();
}

function marcarEnvioEnCurso(enCurso) {
    botonEnviar.disabled = enCurso;
    botonEnviar.textContent = enCurso ? "Enviando..." : "Agregar comentario";
}

formularioComentario.addEventListener("submit", function (evento) {
    evento.preventDefault();
    estadoEnvio.textContent = "";

    const errores = validarComentario();
    mostrarErrores(errores);
    if (Object.keys(errores).length > 0) return;

    marcarEnvioEnCurso(true);
    fetch(formularioComentario.action, { method: "POST", body: new FormData(formularioComentario) })
        .then(function (respuesta) {
            return respuesta.json().then(function (datos) {
                return { ok: respuesta.ok, datos: datos };
            });
        })
        .then(function (resultado) {
            if (!resultado.ok) {
                mostrarErrores(resultado.datos.errores || {});
                estadoEnvio.textContent = resultado.datos.error || "";
                return;
            }
            listaComentarios.prepend(crearItemComentario(resultado.datos.comentario));
            actualizarEstadoVacio();
            formularioComentario.reset();
            estadoEnvio.textContent = "¡Comentario agregado!";
        })
        .catch(function () {
            estadoEnvio.textContent = "No fue posible enviar el comentario. Revisa tu conexión e inténtalo de nuevo.";
        })
        .finally(function () {
            marcarEnvioEnCurso(false);
        });
});

cargarComentarios();
