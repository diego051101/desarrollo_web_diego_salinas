# Observatorio Digital Aviario

Observatorio Digital Aviario es un sitio que registra avistamientos de aves reportados de forma voluntaria en conjunto con la Unión de Ornitólogos de Chile. El proyecto vive en un mismo repositorio que reúne dos entregas distintas, la Tarea 1 como una maqueta estática en HTML, CSS y JavaScript, y la Tarea 2 como un backend real construido con Flask, MySQL y SQLAlchemy sobre esa misma interfaz. Este documento reúne toda la información general de ambas entregas para que cualquiera pueda entender su funcionamiento sin necesitar más contexto.

## Estructura general del repositorio

La siguiente estructura resume las carpetas y archivos principales del repositorio.

```
Desarrollo_Web/
├── html/, css/, js/, json/, recursos/   Tarea 1 (estática)
├── app.py, config.py, models.py, repositorio.py,
│   validaciones.py, requirements.txt   Tarea 2 (Flask)
├── templates/, static/                  Tarea 2 (vistas y recursos servidos por Flask)
├── sql/                                  scripts para crear y poblar la base de datos
└── venv/                                 entorno virtual de Python (no se versiona)
```

Los archivos que pertenecen a la Tarea 1 quedaron completamente intactos durante todo este proceso. La aplicación Flask de la Tarea 2 no depende de ellos en ningún momento porque cuenta con su propia copia de css, js y recursos dentro de la carpeta static, adaptada donde hizo falta. Gracias a esto ambas entregas conviven dentro del mismo repositorio sin interferir entre sí en ningún momento.

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

La Tarea 2 implementa en Python con Flask una parte de las funcionalidades de la Tarea 1 sobre una base de datos real. Cubre la portada con los últimos avistamientos, el registro de voluntarios, el registro de avistamientos con archivos adjuntos y el listado paginado con su vista de detalle, según lo pedido en el enunciado del curso. Las estadísticas quedan pendientes para la siguiente tarea, tal como indica ese mismo enunciado.

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
| `app.py` | Reúne las rutas de Flask y coordina cada petición, delegando la validación y el acceso a datos a otros módulos |
| `models.py` | Define los modelos de SQLAlchemy que reflejan uno a uno las tablas creadas por `tarea2.sql` |
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

## Autor

El sitio fue desarrollado por Diego Salinas para el curso de Desarrollo Web. El diseño visual y la estructura de la Tarea 1 partieron de un proceso de diseño propio, mientras que la Tarea 2 sigue el modelo de datos y las convenciones de Flask y SQLAlchemy que se enseñaron en las clases del curso. Cualquier duda técnica adicional sobre las decisiones tomadas puede resolverse revisando los comentarios que encabezan cada módulo del código.
