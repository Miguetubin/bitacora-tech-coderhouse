from django import forms
from django.core.files.uploadedfile import UploadedFile
from .models import Post


def validate_image(image):
    # Validar la subida nueva sin abrir un archivo previo que podría no existir.
    if isinstance(image, UploadedFile) and image.size > 5 * 1024 * 1024:
        raise forms.ValidationError('La imagen no puede superar los 5 MB.')
    return image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'image']
        widgets = {'content': forms.Textarea(attrs={'rows': 12, 'placeholder': 'Compartí lo que aprendiste…'})}
        help_texts = {'image': 'Opcional. JPG, PNG o WebP. Máximo 5 MB.'}

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if not title:
            raise forms.ValidationError('Escribí un título.')
        return title

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if not content:
            raise forms.ValidationError('Escribí el contenido de la publicación.')
        return content

    def clean_image(self):
        return validate_image(self.cleaned_data.get('image'))
