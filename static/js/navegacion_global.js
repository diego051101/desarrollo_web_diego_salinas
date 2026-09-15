// Script compartido por las plantillas de la Tarea 2 (base.html lo carga en
// todas): resalta el enlace activo del menú, controla el sidebar en modo
// móvil, actualiza el año del footer y le da sombra al header al hacer
// scroll. Es una versión recortada del navegacion_global.js de la Tarea 1:
// se quitaron la inicialización de AOS, el observador de secciones ancla y
// el carrusel automático del hero porque ninguna plantilla de esta tarea
// usa esos elementos (no hay hero ni nav de anclas aquí).

(function marcarEnlaceActivo() {
    // Compara la ruta completa (no solo el nombre de archivo, porque las
    // rutas de Flask son jerárquicas) y elige el enlace cuyo href sea el
    // prefijo más largo de la URL actual — así /avistamientos/7 sigue
    // marcando activo "/avistamientos" sin confundirse con "/avistamientos/nuevo".
    const normalizar = (ruta) => ruta.replace(/\/+$/, "") || "/";
    const rutaActual = normalizar(window.location.pathname);
    const enlaces = document.querySelectorAll("header nav ul a, .barra-lateral a");
    let mejorCoincidencia = null;

    enlaces.forEach(function (enlace) {
        const destino = normalizar(enlace.getAttribute("href"));
        const coincide = destino === "/" ? rutaActual === "/" : rutaActual.startsWith(destino);
        if (coincide && (!mejorCoincidencia || destino.length > mejorCoincidencia.length)) {
            mejorCoincidencia = destino;
        }
    });

    enlaces.forEach(function (enlace) {
        const destino = normalizar(enlace.getAttribute("href"));
        enlace.classList.toggle("activo", mejorCoincidencia !== null && destino === mejorCoincidencia);
    });
})();

(function controlarBarraLateral() {
    const barraLateral = document.getElementById("barra-lateral");
    const botonMenu = document.getElementById("boton-menu-lateral");
    if (!barraLateral || !botonMenu) return;

    function abrirBarra() {
        barraLateral.classList.add("abierta");
        botonMenu.setAttribute("aria-expanded", "true");
    }

    function cerrarBarra() {
        barraLateral.classList.remove("abierta");
        botonMenu.setAttribute("aria-expanded", "false");
    }

    botonMenu.addEventListener("click", function () {
        if (barraLateral.classList.contains("abierta")) {
            cerrarBarra();
        } else {
            abrirBarra();
        }
    });

    barraLateral.querySelectorAll("a").forEach(function (enlace) {
        enlace.addEventListener("click", cerrarBarra);
    });

    document.addEventListener("click", function (evento) {
        const clickFueraDeBarra = !barraLateral.contains(evento.target) && !botonMenu.contains(evento.target);
        if (clickFueraDeBarra) {
            cerrarBarra();
        }
    });

    document.addEventListener("keydown", function (evento) {
        if (evento.key === "Escape") {
            cerrarBarra();
        }
    });
})();

(function actualizarAnioFooter() {
    const elementoAnio = document.getElementById("anio-actual");
    if (!elementoAnio) return;
    elementoAnio.textContent = new Date().getFullYear();
})();

(function elevarHeaderAlHacerScroll() {
    const header = document.querySelector("header");
    if (!header) return;

    function actualizarSombra() {
        header.classList.toggle("con-sombra", window.scrollY > 4);
    }

    window.addEventListener("scroll", actualizarSombra, { passive: true });
    actualizarSombra();
})();
