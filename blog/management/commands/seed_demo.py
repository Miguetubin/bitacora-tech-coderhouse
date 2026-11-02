"""Contenido inicial reproducible sin contraseñas ni imágenes externas."""
from io import BytesIO
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw
from blog.models import Post

ARTICLES = [
    ('Python: de una idea a tu primer programa', 'python',
     'Aprender a programar empieza por resolver problemas pequeños. Python permite concentrarse en la lógica antes de sumar complejidad.\n\nUna buena práctica es separar cada tarea en una función con una responsabilidad clara. Así el código resulta más fácil de leer, reutilizar y probar.\n\nAntes de escribir, definí qué información entra, qué transformación necesitás y qué resultado esperás. Después probá casos normales, datos vacíos y entradas incorrectas.\n\nLa constancia vale más que memorizar sintaxis: construir algo pequeño y entenderlo es un primer paso sólido.'),
    ('Django y el recorrido de una petición web', 'web',
     'Cuando abrís una página, el navegador envía una petición al servidor. En Django, las rutas conectan esa petición con una vista.\n\nLa vista consulta los modelos cuando necesita información y prepara el contexto para un template. El template genera el HTML que vuelve al navegador.\n\nSeparar datos, lógica y presentación ayuda a mantener el proyecto. Un cambio visual no debería obligarte a reescribir una consulta a la base.\n\nPara practicar, seguí una publicación desde su URL hasta el template de detalle. Ese recorrido explica gran parte de la aplicación.'),
    ('Git: documentar el camino también es construir', 'tech',
     'Un repositorio cuenta la historia de un proyecto. Cada commit debería representar un avance real y tener un mensaje que explique qué cambió.\n\nAntes de guardar un cambio, revisá el diff y verificá que no incluya claves, entornos virtuales ni archivos temporales. El archivo .gitignore evita muchos errores, pero no reemplaza esa revisión.\n\nUn README útil completa el trabajo: explica cómo instalar dependencias, preparar la base e iniciar el servidor.\n\nPensá en la persona que clona el proyecto por primera vez. Si puede ejecutarlo sin preguntarte nada, la documentación está cumpliendo su función.'),
]


class Command(BaseCommand):
    help = 'Carga tres artículos de ejemplo e imágenes generadas localmente; se puede repetir sin duplicar.'

    def handle(self, *args, **options):
        User = get_user_model()
        author, created = User.objects.get_or_create(username='bitacora_demo', defaults={'first_name': 'Equipo', 'last_name': 'Bitácora'})
        if created:
            author.set_unusable_password()
            author.save(update_fields=['password'])
        colors = [(210, 233, 166), (198, 216, 236)]
        for index, (title, category, content) in enumerate(ARTICLES):
            post, created = Post.objects.get_or_create(author=author, title=title, defaults={'category': category, 'content': content})
            if created and index < 2:
                image = Image.new('RGB', (1200, 700), colors[index])
                draw = ImageDraw.Draw(image)
                for x in range(0, 1200, 50):
                    draw.line([(x, 0), (x, 700)], fill=(170, 190, 150), width=1)
                for y in range(0, 700, 50):
                    draw.line([(0, y), (1200, y)], fill=(170, 190, 150), width=1)
                draw.rounded_rectangle((340, 190, 860, 510), radius=35, fill=(35, 49, 36))
                draw.text((400, 280), 'PYTHON' if index == 0 else '< / WEB >', fill=colors[index], font_size=72)
                output = BytesIO()
                image.save(output, format='PNG')
                post.image.save(f'demo-{category}.png', ContentFile(output.getvalue()), save=True)
        self.stdout.write(self.style.SUCCESS('Contenido de ejemplo disponible. No se crearon credenciales de acceso.'))
