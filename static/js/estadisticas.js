// Estadísticas (Tarea 3): pide a /api/estadisticas los totales calculados en
// la base de datos y dibuja los tres gráficos con Chart.js. Los colores y la
// tipografía se leen de las variables CSS de global.css para no repetirlos.
const contenedorEstadisticas = document.getElementById("contenedor-estadisticas");
const estadoEstadisticas = document.getElementById("estado-estadisticas");

function leerToken(nombre) {
    return getComputedStyle(document.documentElement).getPropertyValue(nombre).trim();
}

function configurarChart() {
    Chart.defaults.font.family = leerToken("--fuente-texto");
    Chart.defaults.color = leerToken("--color-texto");
    Chart.defaults.maintainAspectRatio = false;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        Chart.defaults.animation = false;
    }
}

// Paleta Okabe-Ito, distinguible con los tipos más comunes de daltonismo.
// Si hay más aves que colores, los siguientes tonos se reparten con el
// ángulo áureo para que ninguna porción repita color.
const PALETA_ACCESIBLE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442", "#000000"];

function coloresDistintos(cantidad) {
    return Array.from({ length: cantidad }, function (_, indice) {
        return PALETA_ACCESIBLE[indice] || `hsl(${Math.round(indice * 137.5) % 360}, 55%, 55%)`;
    });
}

function opcionesConEjes(tituloEjeX, tituloEjeY) {
    return {
        plugins: { legend: { display: false } },
        scales: {
            x: { title: { display: true, text: tituloEjeX } },
            y: { beginAtZero: true, ticks: { precision: 0 }, title: { display: true, text: tituloEjeY } },
        },
    };
}

function dibujarGrafico(idCanvas, tipo, serie, estiloSerie, opciones) {
    const canvas = document.getElementById(idCanvas);
    if (serie.valores.length === 0) {
        const aviso = document.createElement("p");
        aviso.className = "mensaje-estado";
        aviso.textContent = "Todavía no hay datos para este gráfico.";
        canvas.parentElement.replaceWith(aviso);
        return;
    }
    new Chart(canvas, {
        type: tipo,
        data: { labels: serie.etiquetas, datasets: [{ data: serie.valores, ...estiloSerie }] },
        options: opciones,
    });
}

function dibujarEstadisticas(datos) {
    const colorPrincipal = leerToken("--color-principal");
    const colorAcento = leerToken("--color-acento");

    dibujarGrafico(
        "grafico-avistamientos-por-dia",
        "line",
        datos.avistamientos_por_dia,
        { label: "Avistamientos", borderColor: colorPrincipal, backgroundColor: colorPrincipal },
        opcionesConEjes("Día", "Cantidad de avistamientos")
    );
    dibujarGrafico(
        "grafico-avistamientos-por-ave",
        "pie",
        datos.avistamientos_por_ave,
        { label: "Avistamientos", backgroundColor: coloresDistintos(datos.avistamientos_por_ave.valores.length) },
        { plugins: { legend: { position: "bottom" } } }
    );
    dibujarGrafico(
        "grafico-voluntarios-por-comuna",
        "bar",
        datos.voluntarios_por_comuna,
        { label: "Voluntarios", backgroundColor: colorAcento, borderRadius: 4 },
        opcionesConEjes("Comuna", "Cantidad de voluntarios")
    );
}

fetch(contenedorEstadisticas.dataset.url)
    .then(function (respuesta) {
        if (!respuesta.ok) throw new Error(respuesta.status);
        return respuesta.json();
    })
    .then(function (datos) {
        configurarChart();
        dibujarEstadisticas(datos);
        estadoEstadisticas.textContent = "";
    })
    .catch(function () {
        contenedorEstadisticas.hidden = true;
        estadoEstadisticas.textContent = "No fue posible cargar las estadísticas. Recarga la página para intentarlo de nuevo.";
    });
