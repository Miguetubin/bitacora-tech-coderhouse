# Verificación final de Bitácora Tech

Fecha: 2 de noviembre de 2026.

Repositorio: https://github.com/Miguetubin/bitacora-tech-coderhouse

## Instalación y ejecución

- Python 3.12.14 y Django 5.2.18.
- Dependencias instaladas desde `requirements.txt` en entornos virtuales vacíos.
- Primera y segunda revisión local desde copias independientes, sin `.env`, base ni media preexistentes.
- Tercera instalación desde un clon HTTPS del repositorio público de GitHub, con un entorno virtual nuevo.
- Clave local independiente configurada, migraciones aplicadas desde cero y contenido de ejemplo reconstruido.
- `python manage.py check`: sin problemas.
- `python manage.py makemigrations --check --dry-run`: sin cambios pendientes.
- `python manage.py test`: 31 pruebas aprobadas tanto localmente como desde el clon de GitHub.
- Inicio real del servidor con `runserver` comprobado.

## Funcionalidad y permisos

- Verificación HTTP en las dos instalaciones locales: portada, CSS, imágenes demo, redirecciones para visitantes anónimos, registro con sesión, creación/edición/eliminación de publicaciones, perfil, login, logout y búsqueda sin coincidencias.
- Pruebas Django: subida de imágenes y avatar, eliminación de imagen desde formulario, publicaciones sin imagen, validación, búsqueda por título/contenido, paginación, registro y autenticación.
- Usuarios anónimos redirigidos desde las vistas protegidas mediante `@login_required`.
- Usuarios autenticados bloqueados al intentar editar o eliminar publicaciones ajenas.
- Eliminación únicamente por POST, con confirmación previa. CSRF y escape de HTML comprobados.

## Navegador e interfaz

- Recorrido completo con Chromium 153 sobre el clon de GitHub, aprobado dos veces.
- Registro, creación de publicación con imagen, edición, eliminación, perfil con avatar, logout, redirección protegida, login con retorno a la ruta original y búsqueda sin coincidencias.
- Imágenes verificadas como cargadas en el navegador.
- Sin errores JavaScript durante el recorrido.
- Inspección visual de portada en escritorio (1440 px) y celular (390 px), editor, perfil y registro en celular.
- Sin desbordamiento horizontal en portada ni registro en tamaño celular.

## Repositorio y documentación

- Repositorio público, con historial de etapas reales de desarrollo, interfaz, pruebas y documentación.
- Código completo, templates, estáticos y migraciones incluidos.
- Archivos versionados contrastados con el clon descargado desde GitHub al cerrar cada entrega.
- `requirements.txt`, `.gitignore`, `.env.example` y README incluidos.
- README con URL real de clonación, entorno virtual, dependencias, variables, migraciones, servidor, datos demo y superusuario opcional.
- Sin `.env`, claves locales, base de datos, media de prueba, entornos virtuales ni cachés en los archivos versionados.
- Sin rutas absolutas del entorno de trabajo en el código del proyecto.
- La base y las imágenes de ejemplo se reconstruyen con `migrate` y `seed_demo`.

## Revisión ampliada

- Informe detallado y matriz de aceptación en [AUDITORIA.md](AUDITORIA.md).
- Correcciones de imágenes ausentes, recuperación de media demo y textos largos.
- Ocho pantallas comprobadas a 320, 390, 768 y 1440 píxeles.

## Alcance

La entrega solicitada consiste en el repositorio público. La aplicación se ejecuta localmente siguiendo el README; no requiere un servicio de hosting ni un dominio de producción.
