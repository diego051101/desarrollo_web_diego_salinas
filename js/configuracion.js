const formImagen = document.getElementById("form-cambiar-imagen");
const inputImagen = document.getElementById("nueva-imagen");
const formContrasena = document.getElementById("form-cambiar-contrasena");
const inputPassAntigua = document.getElementById("pass-antigua");
const inputPassNueva = document.getElementById("pass-nueva");

formImagen.addEventListener("submit", function(evento) {
    // Evitar default automático.
    evento.preventDefault();
    const archivo = inputImagen.files[0];
    if (!archivo) {
        alert("Selecciona una imagen.");
        return;
    }
    const limiteBytes = 2 * 1024 * 1024;
    if (archivo.size > limiteBytes) {
        alert("El archivo es demasiado pesado.");
        return;
    }
    if (!archivo.type.startsWith('image/')) {
        alert("Formato de archivo inválido.");
        return;
    }
    alert("¡Imagen de perfil actualizada!");
    formImagen.reset();
});

formContrasena.addEventListener("submit", function(evento) {
    // Evitar default automático.
    evento.preventDefault();
    const antigua = inputPassAntigua.value.trim();
    const nueva = inputPassNueva.value.trim();
    if (antigua === "" || antigua.length < 6) {
        alert("Contraseña antigua inválida.");
        return;
    }
    if (nueva === "" || nueva.length < 6 || nueva.length > 30) {
        alert("La contraseña nueva debe tener entre 6 y 30 caracteres.");
        return;
    }
    if (nueva === antigua) {
        alert("La contraseña nueva debe ser distinta a la antigua.");
        return;
    }
    alert("¡Contraseña actualizada con éxito!");
    formContrasena.reset();
});
