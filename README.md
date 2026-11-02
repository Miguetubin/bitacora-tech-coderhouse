# Bitácora Tech

Blog de tecnología desarrollado por **Miguel Tubin** como proyecto final de **Python — Coderhouse**. Permite compartir aprendizajes sobre Python, desarrollo web y tecnología mediante una interfaz en español, adaptable a computadoras y celulares.

## Tecnologías

- Python 3.12 (versión usada para desarrollar y verificar).
- Django 5.2 LTS; versiones exactas de todas las dependencias en `requirements.txt`.
- SQLite para la base de datos de desarrollo.
- Pillow para validar y procesar imágenes.
- python-decouple para configuración mediante variables de entorno.
- HTML y CSS propios; no requiere Node.js ni recursos de un CDN.

## Funcionalidades

- Listado paginado y detalle público de publicaciones.
- Crear, editar y eliminar artículos desde la interfaz web.
- Categorías: Python, desarrollo web y tecnología.
- Imagen opcional de portada con alternativa visual cuando no se carga una.
- Búsqueda por título o contenido, con aviso si no hay coincidencias.
- Registro, login y logout mediante POST.
- Perfil privado, edición de nombre, apellido, correo, biografía y avatar opcional.
- Formularios protegidos con CSRF y contenido escapado en los templates.
- `@login_required` en las vistas de escritura y perfil. Solo el autor puede editar/eliminar sus artículos; una URL ajena devuelve 404.
- Panel administrativo de Django opcional.

## Instalación desde cero

### 1. Clonar y entrar al proyecto

Cloná la URL HTTPS de **este repositorio**, disponible en el botón **Code** de GitHub:

```bash
git clone URL_HTTPS_DE_ESTE_REPOSITORIO bitacora-tech
cd bitacora-tech
```

Reemplazá `URL_HTTPS_DE_ESTE_REPOSITORIO` por la URL real. Los comandos siguientes se ejecutan en la carpeta que contiene `manage.py`.

### 2. Crear y activar un entorno virtual

Windows (PowerShell):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell no permite activar scripts, podés usar CMD:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
```

macOS / Linux, con Python 3.12 instalado:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiá `.env.example` a `.env`:

Windows (PowerShell o CMD):

```bat
copy .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Generá una clave propia:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Pegá el resultado en `SECRET_KEY` dentro de `.env`, reemplazando el marcador. Para las pruebas locales conservá `DEBUG=True` y `ALLOWED_HOSTS=localhost,127.0.0.1,[::1]`.

`.env` no se versiona. `.env.example` solo contiene una plantilla sin secretos reales. La aplicación exige una `SECRET_KEY` configurada y no incluye una clave de respaldo en el código.

### 5. Preparar la base de datos

```bash
python manage.py migrate
```

Las migraciones están incluidas: no es necesario ejecutar `makemigrations` para instalar el proyecto.

### 6. Cargar contenido de ejemplo (opcional, recomendado)

```bash
python manage.py seed_demo
```

Crea tres artículos, dos con imágenes generadas localmente y uno sin imagen. Se puede repetir sin duplicar artículos. El autor de ejemplo tiene una contraseña inutilizable: **no hay credenciales demo**. Registrá tu propia cuenta para probar la escritura.

El repositorio excluye `db.sqlite3` y `media/`. `migrate` reconstruye la base y `seed_demo` reconstruye los ejemplos y sus imágenes sin descargar recursos externos. Sin datos demo, la portada muestra un estado vacío y permite crear la primera publicación.

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

Abrí **http://127.0.0.1:8000/**. Conservá la terminal abierta; para detenerlo usá `Ctrl+C`.

Las imágenes se sirven en desarrollo mediante `MEDIA_URL`, `MEDIA_ROOT` y las rutas condicionales a `DEBUG=True`. Los estáticos se encuentran en `static/`. El servidor de desarrollo no es una configuración de producción.

### 8. Panel administrativo (opcional)

```bash
python manage.py createsuperuser
```

Elegí tus propios datos y contraseña. Luego ingresá en **http://127.0.0.1:8000/admin/**. El CRUD y la autenticación se pueden probar completamente desde la web sin usar el admin.

## Recorrido de prueba manual

1. Sin sesión, visitá la portada, abrí un artículo y buscá palabras de su título y contenido. Buscá también una palabra inexistente.
2. Abrí `/publicaciones/nueva/` y `/cuentas/perfil/` sin sesión: deben redirigir al login.
3. Creá una cuenta en **Crear cuenta**; el registro inicia sesión automáticamente.
4. Entrá en **Escribir**, completá título, categoría y contenido, y cargá una imagen JPG, PNG o WebP de hasta 5 MB. Publicá y verificá la portada y el detalle.
5. Editá el artículo. Probá reemplazar la imagen y luego usar la casilla para quitarla. La página debe seguir funcionando sin imagen.
6. Creá otro artículo sin imagen y verificá su alternativa visual en la portada.
7. En **Mi perfil**, editá tus datos y subí un avatar. Guardá y verificá los cambios. También podés quitarlo.
8. En el detalle de una publicación propia, elegí **Eliminar**: primero aparece una confirmación; solo el botón de confirmación elimina el artículo.
9. Presioná **Salir**. Volvé a una URL de edición/eliminación existente y a `/cuentas/perfil/editar/`: deben pedir login.
10. Ingresá nuevamente. Creá una segunda cuenta y comprobá que no pueda editar/eliminar publicaciones de la primera, incluso escribiendo la URL directamente.

## Verificación automática

Con el entorno activo y `.env` configurado:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Las pruebas crean una base temporal independiente y un directorio temporal para imágenes. Verifican CRUD, imágenes y su eliminación del formulario, validaciones, búsqueda, paginación, registro, login, logout, perfil, permisos, CSRF y escape de HTML. No requieren superusuario ni datos previos.

Para actualizar dependencias, utilizá un entorno virtual exclusivo del proyecto y luego:

```bash
python -m pip freeze > requirements.txt
```

## Estructura

```text
accounts/       Usuarios, perfiles, formularios y pruebas
blog/           Publicaciones, búsqueda, comando demo y pruebas
config/         Settings y rutas principales
static/css/     Estilos propios
templates/      Templates de la interfaz
manage.py       Comandos de Django
requirements.txt
.env.example
.gitignore
README.md
```

## Autor

**Miguel Tubin** · Proyecto final de Python, Coderhouse.

GitHub: [Miguetubin](https://github.com/Miguetubin)
