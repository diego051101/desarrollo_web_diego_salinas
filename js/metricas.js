const inputUsuariosFechaTermino = document.getElementById("usuarios-fecha-termino");
const inputAvistamientosFechaTermino = document.getElementById("avistamientos-fecha-termino");
const fechaHoy = new Date().toISOString().slice(0, 10);

inputUsuariosFechaTermino.value = fechaHoy;
inputAvistamientosFechaTermino.value = fechaHoy;
