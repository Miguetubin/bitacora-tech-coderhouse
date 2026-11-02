# Verificación de Bitácora Tech

Fecha: 2 de noviembre de 2026.

## Comprobado localmente

- Python 3.12.14 y Django 5.2.18.
- Instalación de `requirements.txt` en un segundo entorno virtual vacío.
- Clonado local del repositorio para la segunda revisión, sin `.env`, base ni media.
- Configuración de una clave local independiente, migraciones desde cero y carga de contenido de ejemplo.
- `python manage.py check`: sin problemas.
- `python manage.py makemigrations --check --dry-run`: sin cambios pendientes.
- `python manage.py test`: 16 pruebas aprobadas en el entorno de trabajo y en la instalación limpia.
- Servidor real iniciado con `runserver` en ambas instalaciones.
- Verificación HTTP en ambas instalaciones: portada, CSS, imágenes de ejemplo, redirección del visitante anónimo, registro con sesión, creación/edición/eliminación de publicaciones, edición de perfil, login, logout por POST y búsqueda sin coincidencias.
- Pruebas Django: subida de imágenes de artículos y avatar, eliminación de imagen desde formulario, artículos sin imagen, acceso ajeno bloqueado, CSRF, escape HTML, validación de formularios y paginación.
- Cuatro etapas reales de commits antes de esta consolidación; no se alteraron fechas ni se inventó historial anterior.
- Exclusión de `.env`, entornos, base local, media y cachés del contenido versionado.

## Pendientes antes de entregar

- Revisar visualmente en un navegador de escritorio y celular. El intento de instalar Chromium en el entorno de trabajo falló; las verificaciones HTTP y Django no equivalen a una revisión visual.
- Crear el repositorio público de destino y sincronizar todos los commits.
- Sustituir el marcador de URL de clonación del README por la URL real del repositorio.
- Verificar la visibilidad pública, el contenido remoto y clonar desde GitHub para repetir la instalación final.

Esta lista distingue lo comprobado de lo pendiente. El proyecto no se considera listo para entregar hasta resolver la revisión visual y la verificación remota.
