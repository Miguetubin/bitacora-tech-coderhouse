from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class Post(models.Model):
    class Category(models.TextChoices):
        PYTHON = 'python', 'Python'
        WEB = 'web', 'Desarrollo web'
        TECH = 'tech', 'Tecnología'

    title = models.CharField('título', max_length=160)
    content = models.TextField('contenido')
    category = models.CharField('categoría', max_length=10, choices=Category.choices, default=Category.PYTHON)
    image = models.ImageField('imagen', upload_to='posts/%Y/%m/', blank=True,
                              validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', verbose_name='autor')
    created_at = models.DateTimeField('fecha de publicación', auto_now_add=True)
    updated_at = models.DateTimeField('última edición', auto_now=True)

    class Meta:
        ordering = ['-created_at', '-pk']
        verbose_name = 'publicación'
        verbose_name_plural = 'publicaciones'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
