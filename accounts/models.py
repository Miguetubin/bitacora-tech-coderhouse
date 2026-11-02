from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField('sobre mí', max_length=500, blank=True)
    avatar = models.ImageField('imagen de perfil', upload_to='avatars/%Y/%m/', blank=True,
                               validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])

    def __str__(self):
        return f'Perfil de {self.user.username}'
