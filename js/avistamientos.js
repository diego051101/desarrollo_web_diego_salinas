const botonFiltro = document.getElementById("boton-filtro");
const formularioFiltro = document.getElementById("formulario-filtro");
const botonAplicarFiltro = document.getElementById("boton-aplicar-filtro");
const botonLimpiarFiltro = document.getElementById("boton-limpiar-filtro");
const filasAvistamiento = document.querySelectorAll(".fila-avistamiento");

botonFiltro.addEventListener("click", function() {
    if (formularioFiltro.style.display === "none") {
        formularioFiltro.style.display = "block";
    } else {
        formularioFiltro.style.display = "none";
    }
});

botonAplicarFiltro.addEventListener("click", function() {
    // Filtrado en el listado ya cargado, sin backend.
    const tipo = document.getElementById("filtro-tipo").value.trim().toLowerCase();
    const fecha = document.getElementById("filtro-fecha").value;
    const lugar = document.getElementById("filtro-lugar").value.trim().toLowerCase();
    filasAvistamiento.forEach(function(fila) {
        const coincideTipo = tipo === "" || fila.dataset.tipo.toLowerCase().includes(tipo);
        const coincideFecha = fecha === "" || fila.dataset.fecha === fecha;
        const coincideLugar = lugar === "" || fila.dataset.lugar.toLowerCase().includes(lugar);
        fila.hidden = !(coincideTipo && coincideFecha && coincideLugar);
    });
});

botonLimpiarFiltro.addEventListener("click", function() {
    formularioFiltro.reset();
    filasAvistamiento.forEach(function(fila) {
        fila.hidden = false;
    });
});
