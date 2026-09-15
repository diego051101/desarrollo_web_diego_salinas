// Adaptación de js/registro_usuario.js para la Tarea 2: las regiones ya
// vienen renderizadas por el servidor (Flask consultó la base de datos), así
// que aquí solo falta la cascada región -> comuna, usando el objeto
// `comunasPorRegion` que la plantilla registrar_voluntario.html imprime
// como JSON en vez de pedirlo con fetch (ya no existe regiones_comunas.json
// en esta versión: la información vive en la base de datos).
const formularioRegistro = document.getElementById("formulario-registro");
const selectRegion = document.getElementById("region");
const selectComuna = document.getElementById("comuna");

function llenarComunas(regionId, comunaAPreseleccionar) {
    const comunas = comunasPorRegion[regionId] || [];
    selectComuna.innerHTML = '<option value="" disabled selected>Seleccione comuna...</option>';
    comunas.forEach(function (comuna) {
        const opcion = document.createElement("option");
        opcion.value = comuna.id;
        opcion.textContent = comuna.nombre;
        if (comunaAPreseleccionar && String(comuna.id) === String(comunaAPreseleccionar)) {
            opcion.selected = true;
        }
        selectComuna.appendChild(opcion);
    });
    selectComuna.disabled = comunas.length === 0;
}

selectRegion.addEventListener("change", function () {
    llenarComunas(this.value, null);
});

if (regionSeleccionadaAlCargar) {
    llenarComunas(regionSeleccionadaAlCargar, comunaSeleccionadaAlCargar);
}

formularioRegistro.addEventListener("submit", function (evento) {
    const nombre = document.getElementById("nombre").value.trim();
    const apellido = document.getElementById("apellido").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const telefono = document.getElementById("telefono").value.trim();
    const comuna = selectComuna.value;

    if (nombre === "" || nombre.length < 2 || nombre.length > 50) {
        evento.preventDefault();
        alert("Nombre inválido (debe tener entre 2 y 50 caracteres).");
        return;
    }
    if (apellido === "" || apellido.length < 2 || apellido.length > 50) {
        evento.preventDefault();
        alert("Apellido inválido (debe tener entre 2 y 50 caracteres).");
        return;
    }
    if (correo === "" || !correo.includes("@") || !correo.includes(".") || correo.length < 5 || correo.length > 80) {
        evento.preventDefault();
        alert("Email inválido (máximo 80 caracteres).");
        return;
    }
    const soloNumerosTelefono = telefono.replace(/[+ ]/g, "");
    if (telefono === "" || !/^[0-9]+$/.test(soloNumerosTelefono) || soloNumerosTelefono.length < 8 || telefono.length > 15) {
        evento.preventDefault();
        alert("Teléfono inválido (use solo números, entre 8 y 15 caracteres).");
        return;
    }
    if (comuna === "") {
        evento.preventDefault();
        alert("Debes seleccionar una región y una comuna.");
        return;
    }
    // Todo válido: se deja que el formulario se envíe de verdad a Flask
    // (a diferencia de la Tarea 1, aquí no se hace preventDefault ni reset).
});
