const botonReportarPublicacion = document.getElementById("boton-reportar-publicacion");

botonReportarPublicacion.addEventListener("click", function() {
    // Confirmación antes de reportar.
    const confirmado = confirm("¿Seguro que quieres reportar esta publicación?");
    if (confirmado) {
        alert("Publicación reportada. Nuestro equipo revisará el caso.");
    }
});
