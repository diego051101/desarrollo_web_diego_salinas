// Script compartido por las 10 páginas: navegación activa, sidebar off-canvas,
// scroll reveal (AOS) y sombra de elevación del header.
// No reemplaza ni modifica los scripts propios de cada página.

if (window.AOS) {
    AOS.init({
        duration: 600,
        once: true,
        easing: "ease-out-cubic",
        disable: function () {
            return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        }
    });
}

(function marcarEnlaceActivo() {
    const paginaActual = window.location.pathname.split("/").pop() || "pagina_principal.html";
    const enlaces = document.querySelectorAll("header nav ul a, .barra-lateral a");
    enlaces.forEach(function (enlace) {
        const destino = enlace.getAttribute("href").split("/").pop();
        if (destino === paginaActual) {
            enlace.classList.add("activo");
        }
    });
})();

(function observarSeccionesAncla() {
    const enlacesAncla = document.querySelectorAll('header nav ul a[href^="#"]');
    if (enlacesAncla.length === 0) return;

    const secciones = Array.from(enlacesAncla)
        .map(function (enlace) {
            return document.getElementById(enlace.getAttribute("href").slice(1));
        })
        .filter(Boolean);

    if (secciones.length === 0) return;

    const observador = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (entrada) {
            const enlaceCorrespondiente = document.querySelector('header nav ul a[href="#' + entrada.target.id + '"]');
            if (!enlaceCorrespondiente) return;
            if (entrada.isIntersecting) {
                enlacesAncla.forEach(function (enlace) {
                    enlace.classList.remove("activo");
                });
                enlaceCorrespondiente.classList.add("activo");
            }
        });
    }, { rootMargin: "-40% 0px -50% 0px" });

    secciones.forEach(function (seccion) {
        observador.observe(seccion);
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

(function autoAvanceCarruselHero() {
    const contenedorHero = document.querySelector(".hero-slideshow");
    const botonSiguiente = document.querySelector(".carrusel-siguiente");
    const botonAnterior = document.querySelector(".carrusel-anterior");
    if (!contenedorHero || !botonSiguiente) return;

    const prefiereMovimientoReducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefiereMovimientoReducido) return;

    const intervaloMs = 6000;
    let temporizador = null;

    function detener() {
        if (temporizador) {
            clearInterval(temporizador);
            temporizador = null;
        }
    }

    function iniciar() {
        detener();
        temporizador = setInterval(function () {
            botonSiguiente.click();
        }, intervaloMs);
    }

    // El cambio manual (clic en cualquiera de las flechas) reinicia el conteo,
    // así el avance automático nunca se solapa con la acción del usuario.
    contenedorHero.addEventListener("mouseenter", detener);
    contenedorHero.addEventListener("mouseleave", iniciar);
    contenedorHero.addEventListener("focusin", detener);
    contenedorHero.addEventListener("focusout", iniciar);
    botonSiguiente.addEventListener("click", iniciar);
    if (botonAnterior) {
        botonAnterior.addEventListener("click", iniciar);
    }

    document.addEventListener("visibilitychange", function () {
        if (document.hidden) {
            detener();
        } else {
            iniciar();
        }
    });

    iniciar();
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
