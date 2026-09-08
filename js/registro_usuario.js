const formularioRegistro = document.getElementById("formulario-registro");
const inputPostal = document.getElementById("postal");
const selectRegion = document.getElementById("region");
const selectComuna = document.getElementById("comuna");

let datosRegiones = {};
let datosPostales = {};

Promise.all([
    fetch('../json/regiones_comunas.json').then(respuesta => respuesta.json()),
    fetch('../json/codigos_postales.json').then(respuesta => respuesta.json())
])
.then(([jsonRegiones, jsonPostales]) => {
    datosRegiones = jsonRegiones;
    datosPostales = jsonPostales;
    Object.keys(datosRegiones).forEach(region => {
        const opcion = document.createElement("option");
        opcion.value = region;
        opcion.textContent = region;
        selectRegion.appendChild(opcion);
    });
})
.catch(error => console.error("Error cargando los JSON:", error));

selectRegion.addEventListener("change", function() {
    const regionSeleccionada = this.value;
    const comunas = datosRegiones[regionSeleccionada];
    selectComuna.innerHTML = '<option value="" disabled selected>Seleccione comuna...</option>';  
    if (comunas) {
        comunas.forEach(comuna => {
            const opcion = document.createElement("option");
            opcion.value = comuna;
            opcion.textContent = comuna;
            selectComuna.appendChild(opcion);
        });
        selectComuna.disabled = false;
    }
});

inputPostal.addEventListener("input", function() {
    const codigo = this.value.trim(); 
    if (codigo.length === 7) {
        const ubicacion = datosPostales[codigo];
        if (ubicacion) {
            selectRegion.value = ubicacion.region;
            selectRegion.dispatchEvent(new Event("change"));
            selectComuna.value = ubicacion.comuna;
        }
    }
});

formularioRegistro.addEventListener("submit", function(evento) {
    evento.preventDefault();
    const nombre = document.getElementById("nombre").value.trim();
    const apellido = document.getElementById("apellido").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const postal = document.getElementById("postal").value.trim();
    const region = selectRegion.value;
    const comuna = selectComuna.value;
    if (nombre === "" || nombre.length < 2 || nombre.length > 50) {
        alert("Nombre inválido (debe tener entre 2 y 50 caracteres).");
        return;
    }
    if (apellido === "" || apellido.length < 2 || apellido.length > 50) {
        alert("Apellido inválido (debe tener entre 2 y 50 caracteres).");
        return;
    }
    if (correo === "" || !correo.includes("@") || !correo.includes(".") || correo.length < 5 || correo.length > 254) {
        alert("Email inválido.");
        return;
    }
    if (postal !== "") {
        const esSoloNumeros = /^[0-9]+$/.test(postal);
        if (!esSoloNumeros || postal.length !== 7) {
            alert("Código postal inválido (debe contener exactamente 7 números).");
            return;
        }
    }
    if (region === "" || comuna === "") {
        alert("Debes seleccionar una región y una comuna.");
        return;
    }
    alert("¡Cuenta creada con éxito! Bienvenido a O.D.A.");
    formularioRegistro.reset();
    selectComuna.innerHTML = '<option value="" disabled selected>Primero seleccione región...</option>';
    selectComuna.disabled = true;
});