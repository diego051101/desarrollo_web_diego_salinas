const imagenesCarrusel = document.querySelectorAll(".hero-slideshow img");
const botonCarruselAnterior = document.querySelector(".carrusel-anterior");
const botonCarruselSiguiente = document.querySelector(".carrusel-siguiente");
let indiceCarrusel = 0;

function mostrarSlideCarrusel(indice) {
    imagenesCarrusel.forEach(function(imagen, posicion) {
        imagen.classList.toggle("slide-activo", posicion === indice);
        imagen.classList.toggle("slide-inactivo", posicion !== indice);
    });
}

botonCarruselSiguiente.addEventListener("click", function() {
    indiceCarrusel = (indiceCarrusel + 1) % imagenesCarrusel.length;
    mostrarSlideCarrusel(indiceCarrusel);
});

botonCarruselAnterior.addEventListener("click", function() {
    indiceCarrusel = (indiceCarrusel - 1 + imagenesCarrusel.length) % imagenesCarrusel.length;
    mostrarSlideCarrusel(indiceCarrusel);
});

const formulario = document.getElementById("formulario-contacto");
const selectMotivo = document.getElementById("motivo");
const contenedorOtroMotivo = document.getElementById("contenedor-otro-motivo");
const inputOtroMotivo = document.getElementById("otro-motivo");

fetch('../json/formulario_contacto.json')
    .then(respuesta => respuesta.json())
    .then(datos => {
        Object.entries(datos).forEach(([valor, texto]) => {
            const opcion = document.createElement("option");
            opcion.value = valor;
            opcion.textContent = texto;
            selectMotivo.appendChild(opcion);
        });
    })
    .catch(error => console.error("Error cargando los motivos:", error));

selectMotivo.addEventListener("change", function() {
    if (this.value === "otro") {
        contenedorOtroMotivo.style.display = "block";
    } else {
        contenedorOtroMotivo.style.display = "none";
        inputOtroMotivo.value = ""; // Limpiamos el campo si el usuario se arrepiente
    }
});

formulario.addEventListener("submit", function(evento) {
    // Evitar default automático.
    evento.preventDefault();
    const correo = document.getElementById("correo").value.trim();
    const motivo = document.getElementById("motivo").value;
    const otro_motivo = document.getElementById("otro-motivo").value.trim(); 
    const descripcion = document.getElementById("descripcion").value.trim();
    // Validaciones.
    if (correo === "" || !correo.includes("@") || !correo.includes(".") || correo.length < 5 || correo.length > 254) {
        alert("Email inválido.");
        return;
    }
    // Validamos que haya seleccionado un motivo.
    if (motivo === "") {
        alert("Motivo inválido.");
        return;
    }
    if (motivo === "otro") {
        if (otro_motivo === "" || otro_motivo.length < 5 || otro_motivo.length > 80) {
            alert("Otro motivo inválido.");
            return;
        }
    }
    if (descripcion === "" || descripcion.length < 10 || descripcion.length > 1000) {
        alert("Descripción inválida.");
        return;
    }
    // Mensaje y limpiado.
    alert("¡Contacto exitoso!");
    formulario.reset();
    // Volver a ocultar el campo "Otro".
    contenedorOtroMotivo.style.display = "none";
});