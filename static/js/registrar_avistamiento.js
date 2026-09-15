// Adaptación de js/registro_avistamiento.js para la Tarea 2: el ave ahora
// se elige desde un catálogo (<select>) en vez de escribirse a mano, se
// agrega la validación del voluntario que informa, y el adjunto acepta
// varios archivos a la vez (input multiple), validando cada uno igual que
// antes se validaba el único archivo de la Tarea 1.
const formulario = document.getElementById("formulario-avistamiento");

formulario.addEventListener("submit", function (evento) {
    const voluntario = document.getElementById("voluntario").value;
    const ave = document.getElementById("ave").value;
    const lugar = document.getElementById("lugar").value.trim();
    const fecha = document.getElementById("fecha-ave").value;
    const hora = document.getElementById("hora-ave").value;
    const descripcion = document.getElementById("descripcion").value.trim();
    const archivos = document.getElementById("archivos").files;

    if (voluntario === "") {
        evento.preventDefault();
        alert("Debes seleccionar quién informa el avistamiento.");
        return;
    }
    if (ave === "") {
        evento.preventDefault();
        alert("Debes seleccionar el ave observada.");
        return;
    }
    if (lugar === "" || lugar.length < 2 || lugar.length > 100) {
        evento.preventDefault();
        alert("Lugar inválido.");
        return;
    }
    if (fecha === "" || hora === "") {
        evento.preventDefault();
        alert("Debes ingresar la fecha y la hora.");
        return;
    }
    const fechaAvistamiento = new Date(`${fecha}T${hora}`);
    if (fechaAvistamiento > new Date()) {
        evento.preventDefault();
        alert("Error: la fecha del avistamiento no puede estar en el futuro.");
        return;
    }
    if (descripcion.length > 500) {
        evento.preventDefault();
        alert("La descripción no puede superar los 500 caracteres.");
        return;
    }
    if (archivos.length === 0) {
        evento.preventDefault();
        alert("Adjunte al menos una fotografía o video.");
        return;
    }
    const limiteBytes = 5 * 1024 * 1024;
    for (const archivo of archivos) {
        if (archivo.size > limiteBytes) {
            evento.preventDefault();
            alert(`El archivo "${archivo.name}" es demasiado pesado (máximo 5 MB).`);
            return;
        }
        if (!archivo.type.startsWith("image/") && !archivo.type.startsWith("video/")) {
            evento.preventDefault();
            alert(`El archivo "${archivo.name}" tiene un formato inválido.`);
            return;
        }
    }
    // Todo válido: se deja que el formulario se envíe de verdad a Flask.
});
