# Observatorio Digital Aviario

## Sobre el proyecto

Observatorio Digital Aviario es un sitio web académico que registra avistamientos de aves reportados de forma voluntaria, en conjunto con la Unión de Ornitólogos de Chile.
El sistema permite que una persona cree una cuenta, publique un avistamiento con evidencia fotográfica o de video, y revise el trabajo de otros usuarios mediante un listado filtrable y un panel de métricas.
Todo el comportamiento dinámico corre en el navegador, ya que el proyecto no cuenta con un servidor propio ni con una base de datos real.

## Tecnologías

El proyecto está construido únicamente con HTML5 semántico, CSS3 nativo y JavaScript en su versión ES6, sin frameworks ni librerías externas.
El CSS se apoya en variables definidas en la raíz del documento, además de Flexbox y Grid para armar cada layout, lo que evita depender de utilidades como Bootstrap o Tailwind.
Esta elección busca demostrar dominio de las herramientas base de la plataforma web antes de recurrir a abstracciones de terceros.

## Estructura de carpetas

El repositorio separa el código según su naturaleza en lugar de mezclar todo dentro de una sola carpeta.
La carpeta html reúne las diez páginas del sitio, css contiene un archivo por cada módulo visual, js aporta un archivo por cada página que necesita lógica propia, json guarda los datos simulados que consumen los formularios, recursos almacena las imágenes e íconos, y wireframes conserva los bocetos que guiaron cada pantalla.
Esta separación permite ubicar cualquier archivo por su función sin depender de nombres largos ni de rutas confusas.

```
html
css
js
json
recursos
wireframes
```

## Paleta de colores

La paleta se compone de cinco colores tomados directamente del enunciado de la tarea, cada uno con una función fija dentro de la interfaz.
El crema FBF7EF ocupa el fondo general, el verde claro BED784 cubre las superficies y tarjetas, el marrón oscuro 0E0B06 se usa en el texto, el verde profundo 396A45 marca la identidad principal y el naranjo E3714F resalta las llamadas a la acción.
Esta distribución sigue la regla de sesenta, treinta y diez que suele recomendarse en diseño de interfaces, donde un color domina la composición, otro la acompaña y el tercero se reserva para acentos puntuales.

Los colores rojo, verde oscuro, blanco y gris que aparecen fuera de esa paleta se reservan para mensajes de validación y texto secundario, tal como lo permite el enunciado original.

## Tipografía

La tipografía se apoya en dos familias que se reparten roles distintos dentro del documento.
Amaranth aparece en todos los títulos gracias a su trazo con más carácter, mientras que Open Sans se aplica al cuerpo de texto por su lectura cómoda en bloques largos.
Ambas fuentes se cargan desde Google Fonts en el archivo global, por lo que basta una sola línea para que todo el sitio las herede.

## Páginas del sitio

El sitio se divide en diez páginas que replican el recorrido real de una persona que visita el observatorio.
Existen dos versiones de la página principal, una para quien no ha iniciado sesión y otra para quien sí, además de las pantallas de registro, inicio de sesión, perfil, configuración, publicación de avistamientos, listado de avistamientos, métricas y detalle de una publicación.
Cada página carga solo los archivos de estilo y de lógica que necesita, lo que evita peso innecesario en el navegador.

1. pagina_principal.html, presenta el proyecto a un visitante sin cuenta.
2. pagina_principal_sesion_iniciada.html, la misma página principal con el encabezado ajustado a un usuario con sesión activa.
3. inicio_sesion.html, formulario de ingreso simulado.
4. registro_usuario.html, formulario de creación de cuenta.
5. registro_avistamiento.html, formulario para publicar un avistamiento.
6. perfil.html, muestra la información pública de un usuario.
7. configuracion.html, permite cambiar la imagen de perfil y la contraseña.
8. avistamientos.html, listado filtrable con paginación.
9. metricas.html, indicadores de usuarios y avistamientos.
10. publicacion.html, vista detallada de un avistamiento.

## Datos simulados

Como el proyecto no tiene backend, los datos que normalmente vendrían de una base de datos se sirven desde archivos JSON ubicados en la carpeta json.
regiones_comunas.json entrega las dieciséis regiones de Chile con sus comunas para llenar los selectores del formulario de registro, codigos_postales.json permite autocompletar región y comuna a partir de un código postal, y formulario_contacto.json llena el selector de motivo del formulario de contacto.
Estos archivos se consultan con fetch de forma asíncrona, así que cada formulario se llena recién cuando la respuesta llega.

## Validaciones

Cada formulario del sitio valida sus propios datos en el navegador antes de simular un envío.
Los controles revisan formato de correo, longitud mínima y máxima de texto, tipo y peso de los archivos adjuntos, y que la fecha de un avistamiento no quede en el futuro.
Cuando algo falla se muestra una alerta clara y el formulario no continúa, de modo que la persona siempre sabe qué corregir.

## Accesibilidad y diseño responsivo

La interfaz agrega estados de foco visibles solo para navegación por teclado, junto con suficiente contraste entre texto y fondo en cada combinación de color usada.
El documento incluye la etiqueta viewport necesaria para que las consultas de medios funcionen en un teléfono real, y cada hoja de estilo trae su propio punto de quiebre para reordenar el contenido en pantallas angostas.
El resultado es una interfaz que se puede usar con mouse, teclado o pantalla táctil sin perder claridad.

## Cómo ejecutar el proyecto

El sitio no requiere instalación ni dependencias, por lo que abrir cualquier archivo html en un navegador ya permite recorrerlo.
Para que los formularios que dependen de fetch funcionen sin problemas conviene servir la carpeta desde un servidor local simple, por ejemplo con la extensión Live Server o con el módulo http.server de Python.
Una vez levantado el servidor basta con entrar a html/pagina_principal.html para comenzar la navegación.

## Autor

El sitio fue desarrollado por Diego Salinas como entrega de la Tarea 1 del curso de Desarrollo Web.
El diseño visual, la estructura del código y el contenido de cada página se definieron a partir de wireframes propios y de los lineamientos de marca establecidos al inicio del proyecto.
Cualquier duda sobre una decisión técnica puede resolverse revisando los comentarios cortos que acompañan cada archivo JavaScript.
