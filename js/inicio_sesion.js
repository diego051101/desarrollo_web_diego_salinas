const formularioInicioSesion = document.getElementById("formulario-inicio-sesion");

formularioInicioSesion.addEventListener("submit", function(evento) {
    // Evitar default automático.
    evento.preventDefault();
    const correo = document.getElementById("correo").value.trim();
    const contrasena = document.getElementById("contrasena").value.trim();
    if (correo === "" || !correo.includes("@") || !correo.includes(".") || correo.length < 5 || correo.length > 254) {
        alert("Email inválido.");
        return;
    }
    if (contrasena === "" || contrasena.length < 6) {
        alert("Contraseña inválida.");
        return;
    }
    // Es un mockup sin backend, así que cualquier dato válido inicia sesión.
    window.location.href = "pagina_principal_sesion_iniciada.html";
});
