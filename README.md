# Observatorio Digital Aviario

Observatorio Digital Aviario es un sitio que registra avistamientos de aves reportados de forma voluntaria en conjunto con la Unión de Ornitólogos de Chile. El proyecto vive en un mismo repositorio que reúne tres entregas, la Tarea 1 como una maqueta estática en HTML, CSS y JavaScript, la Tarea 2 como un backend real construido con Flask, MySQL y SQLAlchemy sobre esa misma interfaz, y la Tarea 3 como la ampliación de ese backend con estadísticas y comentarios. Este documento reúne la información general de las tres entregas para que cualquiera pueda entender su funcionamiento sin necesitar más contexto.

## Estructura general del repositorio

La siguiente estructura resume las carpetas y archivos principales del repositorio.

```
Desarrollo_Web/
├── html/, css/, js/, json/, recursos/   Tarea 1 (estática)
├── app.py, config.py, models.py, repositorio.py,
│   validaciones.py, requirements.txt   Tareas 2 y 3 (Flask)
├── templates/, static/                  Tareas 2 y 3 (vistas y recursos servidos por Flask)
├── sql/                                  scripts para crear y poblar la base de datos
└── venv/                                 entorno virtual de Python (no se versiona)
```

Los archivos que pertenecen a la Tarea 1 quedaron completamente intactos durante todo este proceso. La aplicación Flask de las Tareas 2 y 3 no depende de ellos porque cuenta con su propia copia de css, js y recursos dentro de la carpeta static, adaptada donde hizo falta. Gracias a esto la maqueta estática y la aplicación conviven dentro del mismo repositorio sin interferir entre sí.

Todas las imágenes del proyecto se guardan en formato webp en lugar de jpg o png. Ese formato comprime mucho mejor sin perder calidad visible y por eso el peso total de las carpetas de recursos bajó a menos de la mitad. Gracias a ese cambio la página carga más rápido para quien la visita y el repositorio pesa menos para quien lo descarga.

## Tarea 1, maqueta estática con HTML5, CSS3 y JavaScript

### Tecnologías

La maqueta está construida únicamente con HTML5 semántico, CSS3 nativo y JavaScript en su versión ES6, sin ningún framework de interfaz. El CSS se apoya en variables definidas en el archivo global, además de Flexbox y Grid para armar cada uno de los layouts de la página. La única dependencia externa de esta parte del proyecto es la librería AOS, cargada por CDN, que se usa para las animaciones de aparición al hacer scroll.

### Estructura de carpetas

La carpeta raíz de la Tarea 1 organiza sus archivos de la siguiente forma.

- `html/` reúne las 10 páginas del sitio.
- `css/` contiene 8 hojas de estilo, una por cada módulo visual, y `global.css` reúne lo compartido entre páginas como las variables, el header, el sidebar, el footer y la tipografía base.
- `js/` aporta un archivo por cada página que necesita lógica propia, además de `navegacion_global.js`, que comparten las 10 páginas para la navegación activa, el sidebar en el celular, el carrusel automático del hero y el año del footer.
- `json/` guarda los datos simulados que consumen los formularios a través de fetch, como las regiones y comunas, los códigos postales y los motivos del formulario de contacto.
- `recursos/` almacena las imágenes, los logos y los íconos del sitio.

### Paleta y tipografía

La paleta combina cinco colores siguiendo la regla de sesenta, treinta y diez que suele recomendarse en diseño de interfaces. El fondo usa el crema FBF7EF, las superficies el verde claro BED784, el texto el marrón oscuro 0E0B06, el color principal el verde profundo 396A45 y el acento el naranjo E3714F. Los títulos usan la tipografía Amaranth y el cuerpo de texto usa Open Sans, ambas cargadas desde Google Fonts.

### Páginas del sitio

El sitio reparte su contenido en diez páginas que replican el recorrido real de una persona que lo visita.

1. `pagina_principal.html`, presenta el proyecto a un visitante sin cuenta.
2. `pagina_principal_sesion_iniciada.html`, la misma página principal con el encabezado ajustado a un usuario con sesión activa.
3. `inicio_sesion.html`, formulario de ingreso simulado.
4. `registro_usuario.html`, formulario de creación de cuenta.
5. `registro_avistamiento.html`, formulario para publicar un avistamiento.
6. `perfil.html`, muestra la información pública de un usuario.
7. `configuracion.html`, permite cambiar la imagen de perfil y la contraseña.
8. `avistamientos.html`, listado filtrable con paginación.
9. `metricas.html`, indicadores de usuarios y avistamientos.
10. `publicacion.html`, vista detallada de un avistamiento.

### Validaciones, accesibilidad y responsividad

Cada formulario del sitio valida sus propios datos en el navegador antes de simular un envío, revisando el formato del correo, la longitud del texto y el peso de los archivos adjuntos. La interfaz agrega estados de foco visibles solo para quienes navegan con teclado y etiquetas aria en los controles que no tienen texto visible, y respeta siempre la preferencia de movimiento reducido en cualquier animación. Cada hoja de estilo define sus propios puntos de quiebre para pantallas angostas, y el sidebar de las páginas con sesión iniciada colapsa a un menú desplegable en el celular.

### Cómo ejecutar la Tarea 1

La Tarea 1 no requiere ninguna instalación para poder revisarla. Basta con abrir el archivo `pagina_principal.html` directamente en un navegador para recorrer todo el sitio sin problema. Si se prefiere que los fetch hacia los archivos JSON funcionen sin restricciones, conviene servir la carpeta con un servidor estático simple como el módulo `http.server` de Python.

## Tarea 2, backend con Flask, MySQL y SQLAlchemy

La Tarea 2 implementa en Python con Flask una parte de las funcionalidades de la Tarea 1 sobre una base de datos real. Cubre la portada con los últimos avistamientos, el registro de voluntarios, el registro de avistamientos con archivos adjuntos y el listado paginado con su vista de detalle, según lo pedido en el enunciado del curso. Las estadísticas quedaron pendientes para la Tarea 3, tal como indicaba ese mismo enunciado.

### Cómo ejecutarlo

La aplicación se levanta siguiendo estos pasos.

1. Crear la base de datos, para lo cual se requiere un usuario con privilegios de administrador en MySQL, ya que las credenciales de la propia aplicación las crea el script.
   ```
   mysql -u root -p < sql/tarea2.sql
   mysql -u root -p tarea2 < sql/region-comuna.sql
   mysql -u root -p tarea2 < sql/aves.sql
   ```
2. Instalar las dependencias con Python 3.10 o superior mediante `pip install -r requirements.txt`.
3. Ejecutar `python app.py` y abrir `http://127.0.0.1:5000/` en el navegador.

La cadena de conexión por defecto en `config.py` usa exactamente las credenciales que exige el enunciado, con el usuario `cc5002`, la contraseña `programacionweb`, el host `localhost`, el puerto 3306 y la base `tarea2`. Ese valor se puede sobreescribir con la variable de entorno `DATABASE_URL` sin tocar ninguna línea de código. Gracias a esto fue posible probar todo el flujo contra una base SQLite temporal antes de usar la base MySQL real.

### Estructura del código

La siguiente tabla resume la responsabilidad de cada archivo principal del backend.

| Archivo | Responsabilidad |
|---|---|
| `app.py` | Reúne las rutas de Flask, incluidas las rutas `/api/` de la Tarea 3, y coordina cada petición delegando la validación y el acceso a datos |
| `models.py` | Define los modelos de SQLAlchemy que reflejan uno a uno las tablas creadas por `tarea2.sql` y `tabla-comentario.sql` |
| `repositorio.py` | Reúne todas las consultas y escrituras hacia la base de datos, sin que `app.py` necesite conocer ninguna línea de SQL |
| `validaciones.py` | Reúne las reglas de validación del servidor, replicando las mismas reglas que ya existían en JavaScript |
| `config.py` | Reúne la conexión a la base de datos, la carpeta de subidas y los límites de tamaño, extensión y paginación |
| `sql/` | Reúne los scripts que crean el esquema y cargan los catálogos de región, comuna y ave antes de levantar la aplicación |
| `templates/` | Reúne las vistas de Jinja, todas heredando de `base.html` para no repetir el header, el sidebar y el footer en cada página |
| `static/` | Reúne una copia adaptada de los recursos visuales de la Tarea 1, además de la carpeta `uploads` donde se guardan los archivos que suben los usuarios |

### Decisiones sobre el modelo de datos

El enunciado permite ajustar el modelo propuesto a las decisiones ya tomadas en la Tarea 1, y estos fueron los ajustes concretos que se hicieron.

- La columna `voluntario.nombre` es una sola en la base de datos, así que se mantuvieron los campos de nombre y apellido por separado en el formulario junto con sus validaciones, y el servidor los concatena en un solo texto antes de guardar.
- La columna `voluntario.telefono` es obligatoria en la base de datos aunque el formulario de la Tarea 1 no la pedía, así que se agregó ese campo de forma obligatoria, validando que contenga solo dígitos entre 8 y 15 caracteres.
- El código postal no tiene ninguna columna donde guardarse en el modelo de la Tarea 2, así que se eliminó del formulario porque en la Tarea 1 solo autocompletaba región y comuna sin persistirse en ningún lado.
- La tabla `ave` solo tiene la columna nombre sin ninguna columna de tipo, así que el campo de texto libre para el nombre del ave pasó a ser un selector con el catálogo ya cargado en la base de datos, eliminando el campo de tipo por no tener dónde persistirse.
- La columna `avistamiento.fecha_hora` es un único valor de fecha y hora, así que el formulario conserva los campos separados de fecha y hora de la Tarea 1 y el servidor los combina antes de guardar.
- Como esta tarea no pide implementar un inicio de sesión, el formulario para informar un avistamiento incluye un selector con los voluntarios ya registrados, y al terminar de registrarse se ofrece un enlace directo para registrar un avistamiento que llega con ese voluntario ya preseleccionado.
- El formulario permite adjuntar varios archivos a la vez gracias al atributo `multiple`, y el servidor inserta una fila en la tabla `registro` por cada archivo válido que recibe.

### Validación y seguridad

La seguridad de esta parte del proyecto se sostiene sobre varias capas independientes entre sí.

- Todas las reglas que ya existían en JavaScript se mantuvieron, adaptadas en los archivos `registrar_voluntario.js` y `registrar_avistamiento.js` dentro de `static`, mientras que los archivos originales de la Tarea 1 no se tocaron en ningún momento y ahora dejan que el formulario se envíe de verdad al servidor cuando la validación pasa.
- Esas mismas reglas se repiten en el servidor porque el formulario del navegador se puede saltar por completo con una petición directa, así que cualquier identificador recibido para una comuna, un voluntario o un ave se valida contra los identificadores reales que existen en la base de datos.
- El conversor entero de Flask rechaza automáticamente cualquier valor no numérico dentro de la URL, y el número de página del listado siempre se acota a un rango válido sin importar qué llegue en ese parámetro.
- Las consultas siempre pasan por el ORM de SQLAlchemy sin concatenar nunca texto del usuario dentro de una consulta, lo que evita la inyección SQL por diseño, mientras que Jinja escapa automáticamente cualquier variable impresa en una plantilla, lo que evita el XSS.
- Los archivos adjuntos se validan por su extensión permitida, por su tamaño máximo de 5 megabytes y por el tipo real de su contenido usando la librería `filetype`, y el nombre final se pasa por `secure_filename` sumado a un prefijo único antes de guardarse.

### Validación W3C

Se validó el HTML ya renderizado de las 7 páginas del backend contra el validador oficial de W3C durante todo el desarrollo. Se hizo lo mismo con las 7 hojas de estilo que usa esa parte del proyecto, esta vez contra el validador oficial de CSS de W3C. En ambos casos el resultado fue de cero errores encontrados.

## Tarea 3, estadísticas y comentarios

La Tarea 3 completa sobre la misma aplicación Flask las estadísticas que la Tarea 1 solo había maquetado y agrega comentarios a cada avistamiento. Ambas funcionalidades se construyen en el navegador con JavaScript y la función fetch, que consulta rutas del servidor dedicadas a entregar datos en formato JSON. La base de datos sigue siendo la de la Tarea 2, con la única adición de la tabla comentario que acompaña al enunciado.

### Cómo ejecutarla

La Tarea 3 no modifica ninguna tabla existente, así que basta con agregar la tabla comentario sobre la base de datos ya creada para la Tarea 2. El archivo `sql/tabla-comentario.sql` es una copia exacta del script entregado con el enunciado y se ejecuta con el comando que sigue. En una instalación desde cero se corren primero los tres scripts de la Tarea 2 y después este.

```
mysql -u root -p tarea2 < sql/tabla-comentario.sql
```

### Rutas de datos

El servidor expone tres rutas que responden en JSON, resumidas en la tabla siguiente.

| Ruta | Método | Respuesta |
|---|---|---|
| `/api/estadisticas` | GET | Las tres series de los gráficos, cada una como etiquetas y valores |
| `/api/avistamientos/<id>/comentarios` | GET | Los comentarios del avistamiento, del más reciente al más antiguo |
| `/api/avistamientos/<id>/comentarios` | POST | 201 con el comentario creado, 422 con los errores por campo o 404 si el avistamiento no existe |

Los códigos de estado siguen su significado estándar, de modo que el JavaScript distingue un error de validación de un avistamiento inexistente sin interpretar el texto de la respuesta. El conversor entero de Flask rechaza cualquier identificador que no sea numérico antes de que llegue a una consulta. Cada ruta delega el acceso a datos en `repositorio.py` y la validación en `validaciones.py`, igual que las páginas de la Tarea 2.

### Gráficos

Los gráficos se dibujan con [Chart.js](https://www.chartjs.org/) 4.4.1, publicado bajo licencia MIT, que permite su uso libre en cualquier proyecto. Se prefirió a Highcharts porque su licencia gratuita se limita al uso no comercial, y a Flot porque depende de jQuery, una biblioteca que el resto del sitio no necesita. Chart.js se carga desde cdnjs con un hash de integridad, que impide al navegador ejecutarlo si el archivo servido fuera alterado.

Las tres consultas agrupan y cuentan directamente en la base de datos, de modo que el servidor envía solo los totales y nunca las filas completas. El gráfico de líneas cuenta los avistamientos según su fecha de observación, porque la tabla avistamiento no guarda una fecha de registro distinta, y completa con cero los días sin avistamientos para no unir dos días lejanos como si fueran consecutivos. El gráfico de barras muestra solo las comunas que tienen voluntarios, ordenadas alfabéticamente, tal como pide el enunciado.

Los colores de la línea y de las barras se leen de las variables CSS del sitio, así que cualquier cambio en la paleta alcanza también a los gráficos. La torta usa la paleta Okabe-Ito, diseñada para que sus colores se distingan con los tipos más comunes de daltonismo. Las animaciones se desactivan cuando el sistema operativo del visitante declara preferencia por movimiento reducido.

### Comentarios

El formulario de cada avistamiento pide el nombre de quien comenta, entre 3 y 50 caracteres, y el texto del comentario, entre 5 y 300 caracteres, en un área de texto de 3 filas y 40 columnas. El enunciado no fija un máximo para el texto, así que se usó el límite de la columna `comentario.texto`, definida como VARCHAR(300). Ambos rangos viven en `config.py` y la plantilla los imprime como atributos `minlength` y `maxlength`, que el JavaScript lee para validar con exactamente las mismas reglas que el servidor.

Cuando la validación del navegador falla, el mensaje aparece junto al campo afectado y no se envía nada. Si los datos pasan, el formulario se envía con fetch y el servidor vuelve a validarlos desde cero, porque una petición directa puede saltarse el JavaScript por completo. Si el servidor los rechaza, responde con los mismos mensajes por campo y el formulario permanece visible con lo escrito para que pueda corregirse.

El servidor asigna la fecha del comentario al guardarlo y rechaza los emojis, que el juego de caracteres utf8 de la base de datos no puede almacenar. El JavaScript inserta el nombre y el texto en la página como texto plano y nunca como HTML, por lo que un comentario con etiquetas script se muestra literalmente sin ejecutarse. El botón de envío se deshabilita mientras la petición está en curso, lo que evita guardar el mismo comentario dos veces por un doble clic.

### Mejoras al código de la Tarea 2

La revisión del proyecto durante esta entrega detectó y corrigió los siguientes problemas del código anterior:

- El avistamiento y sus archivos adjuntos se guardaban con confirmaciones separadas, y ahora se guardan en una sola transacción.
- El listado consultaba los archivos de cada avistamiento por separado, y ahora los precarga en una consulta fija.
- Las páginas no tenían un título principal `h1`, salvo la portada, y los títulos del pie de página saltaban niveles.
- El contenido principal ocupaba solo el ancho de su contenido en escritorio, en lugar del ancho disponible.
- El texto gris de las tarjetas de la portada no alcanzaba el contraste mínimo de 4,5 a 1 sobre el fondo verde.
- El enlace de correo del pie de página apuntaba a una dirección distinta de la que mostraba.
- Los estilos escritos dentro del HTML pasaron a una clase reutilizable, y las validaciones y rutas repetidas se extrajeron a funciones comunes.

### Validación W3C de la Tarea 3

Se validó el HTML ya renderizado de las 7 páginas de la aplicación contra el validador oficial de W3C, con cero errores y cero advertencias. Se hizo lo mismo con las 9 hojas de estilo de la carpeta static contra el validador oficial de CSS, también con cero errores. Ambas validaciones se repitieron después de cada cambio de estructura, porque corregir la jerarquía de títulos llegó a introducir un error que el validador detectó a tiempo.

## Autor

El sitio fue desarrollado por Diego Salinas para el curso de Desarrollo Web. El diseño visual y la estructura de la Tarea 1 partieron de un proceso de diseño propio, mientras que las Tareas 2 y 3 siguen el modelo de datos y las convenciones de Flask y SQLAlchemy que se enseñaron en las clases del curso. Cualquier duda técnica adicional sobre las decisiones tomadas puede resolverse revisando los comentarios que encabezan cada módulo del código.
