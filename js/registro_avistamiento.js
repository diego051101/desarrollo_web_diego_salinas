const formulario = document.getElementById("formulario-avistamiento");

formulario.addEventListener("submit", function(evento) {
    // Evitar default automático.
    evento.preventDefault();
    // Valores.
    const nombre = document.getElementById("nombre-ave").value.trim();
    const tipo = document.getElementById("tipo-ave").value.trim();
    const lugar = document.getElementById("lugar-ave").value.trim();
    const hora = document.getElementById("hora-ave").value;
    const fecha = document.getElementById("fecha-ave").value;
    const evidencia = document.getElementById("evidencia");
    const archivo = evidencia.files[0];
    // Validación strings.
    if (nombre === "" || nombre.length > 42 || nombre.length < 2) {
        alert("Nombre inválido.");
        return;
    }
    if (tipo === "" || tipo.length > 60 || tipo.length < 2) {
        alert("Tipo inválido.");
        return;
    }
    if (lugar === "" || lugar.length > 100 || lugar.length < 2) {
        alert("Lugar inválido.");
        return;
    }
    if (fecha === "" || hora === "") {
        alert("Debes ingresar la fecha y la hora.");
        return;
    }
    // Validación timestamp.
    const fechaAvistamiento = new Date(`${fecha}T${hora}`);
    const fechaActual = new Date();
    if (fechaAvistamiento > fechaActual) {
        alert("Error: la fecha del avistamiento no puede estar en el futuro.");
        return;
    }
    if (!archivo) {
        alert("Adjunte una fotografía o video.");
        return;
    }
    // Validación tamaño archivo y formato.
    const limiteBytes = 5 * 1024 * 1024;
    if (archivo.size > limiteBytes) {
        alert("El archivo es demasiado pesado.");
        return;
    }
    if (!archivo.type.startsWith('image/') && !archivo.type.startsWith('video/')) {
        alert("Formato de archivo inválido.");
        return;
    }
    // Mensaje y limpiado.
    alert("¡Avistamiento enviado!");
    formulario.reset();
});