const botonReportar = document.getElementById("boton-reportar");
const botonVerMas = document.querySelector(".boton-ver-mas");

botonReportar.addEventListener("click", function() {
    // Confirmación antes de reportar.
    const confirmado = confirm("¿Seguro que quieres reportar a este usuario?");
    if (confirmado) {
        alert("Usuario reportado. Nuestro equipo revisará el caso.");
    }
});

botonVerMas.addEventListener("click", function() {
    // Mock sin más publicaciones cargadas.
    alert("No hay más publicaciones por el momento.");
});
