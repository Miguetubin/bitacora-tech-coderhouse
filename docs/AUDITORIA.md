# Auditoría de entrega — Bitácora Tech

Revisión ampliada: 2 de noviembre de 2026.

Base de evaluación: la consigna de entrega final de Python / Coderhouse proporcionada por Miguel Tubin. El alcance se conserva: blog Django, repositorio público y ejecución local por un tercero.

## Hallazgos y correcciones

| Caso encontrado | Corrección | Verificación |
| --- | --- | --- |
| Un archivo eliminado de `media/` dejaba una imagen rota en la portada, el detalle o el perfil. | Los templates comprueban la disponibilidad del archivo y muestran la alternativa sin imagen. | Pruebas con referencia en la base y archivo físico eliminado. |
| Editar datos conservando una imagen cuyo archivo ya no estaba disponible podía consultar su tamaño y fallar. | El límite de tamaño se valida sobre las nuevas subidas, sin abrir archivos antiguos. | Edición de artículo y perfil con el archivo original ausente. |
| Repetir `seed_demo` no recuperaba imágenes de ejemplo perdidas si los artículos ya existían. | El comando repone las imágenes ausentes y conserva los artículos existentes. | Ejecución, eliminación de imágenes, nueva ejecución y control de duplicados. |
| Nombres, biografías, títulos o nombres de archivo largos podían desbordar pantallas pequeñas. | Ajustes de salto de texto, reducción de título en celulares pequeños y distribución de controles. | Ocho pantallas en cuatro anchos: 32 combinaciones sin desbordamiento horizontal. |

## Matriz de aceptación

| Requisito de la consigna | Resultado de la revisión |
| --- | --- |
| Listado y detalle de publicaciones desde la web | Comprobados con visitante anónimo y en navegador. |
| Crear, editar y eliminar desde la interfaz | Recorrido completo; confirmación antes de eliminar y eliminación por POST. |
| Cargar y mostrar imagen del post | PNG, JPG y WebP verificados; subida real desde navegador. |
| Template resistente sin imagen | Publicación sin imagen y archivo desaparecido comprobados. |
| Registro, login y logout | Flujos correctos; errores de credenciales y registro inválido comprobados. |
| Perfil accesible | Perfil propio y listado de sus publicaciones comprobados. |
| Editar perfil y avatar, si se implementaron | Edición, subida, eliminación del avatar y validaciones comprobadas. |
| Diferencia entre visitante y usuario autenticado | Navegación y rutas verificadas en ambos estados. |
| Protección en las vistas | `@login_required` en creación, edición, eliminación, perfil y edición de perfil. |
| Prohibición de modificar publicaciones ajenas | GET y POST bloqueados aunque se escriba directamente la URL. |
| Configuración de estáticos y media | `STATIC_URL`, `MEDIA_URL`, `MEDIA_ROOT` y rutas de desarrollo revisados. |
| Búsqueda, si se implementó | Título, contenido, consulta vacía, sin resultados y escape de HTML verificados. |
| Repositorio público | Visibilidad comprobada mediante GitHub y clonación HTTPS. |
| Código, apps, templates y estáticos | Incluidos en el contenido versionado. |
| Migraciones finales incluidas | Migración desde base vacía y ausencia de cambios pendientes comprobadas. |
| requirements.txt actualizado | Entorno exclusivo; instalación y `pip check` sin conflictos. |
| README completo | Autor, tecnologías, funciones, instalación, entorno virtual, dependencias, variables, migraciones, servidor y superusuario opcional. |
| Variables y secretos | `.env.example` sin valores privados; `.env` excluido y clave leída desde la configuración local. |
| .gitignore y limpieza | Entornos, cachés, base, media, temporales y configuración del editor excluidos. |
| BASE_DIR y portabilidad | Configuración sin rutas absolutas de la computadora de desarrollo. |
| Historial con progreso | Etapas de base, interfaz, pruebas, documentación y correcciones reales. |
| Reconstrucción sin db.sqlite3 ni media | `migrate` y `seed_demo`; no requiere descargar imágenes externas. |
| Cambios disponibles en GitHub | Publicación y contraste remoto al cerrar la auditoría. |

## Pruebas ampliadas

La suite contiene **31 pruebas**. Además del recorrido principal, comprueba:

- Formularios vacíos, título demasiado largo, contenido en blanco y categoría inválida.
- Archivo que finge ser una imagen, extensión no admitida e imágenes de más de 5 MB.
- Conservación de la imagen al editar, reemplazo y eliminación desde formulario.
- Conservación de datos anteriores ante un formulario inválido, sin guardados parciales del perfil.
- Intentos de alterar autor, usuario, nombre de cuenta o permisos de administrador mediante campos adicionales.
- CSRF en registro, login, logout, publicación, edición, eliminación y edición de perfil.
- Redirección de login segura, paginación con valores inválidos y escape de contenido HTML.
- Acceso al panel administrativo restringido al personal autorizado.
- Estado vacío del blog y página 404 personalizada.

## Límites de la revisión

La ejecución se comprueba en Linux con Python 3.12 y Chromium. El README también incluye comandos de Windows, pero no se ejecutó una sesión de Windows. El proyecto se entrega para desarrollo local; no se certifica una configuración de producción. La calificación corresponde al evaluador y no puede garantizarse.
