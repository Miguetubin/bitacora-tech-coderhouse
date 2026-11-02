from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blog.forms import validate_image
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico', required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserForm(forms.ModelForm):
    email = forms.EmailField(label='Correo electrónico', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {'bio': forms.Textarea(attrs={'rows': 4})}
        help_texts = {'avatar': 'Opcional. JPG, PNG o WebP. Máximo 5 MB.'}

    def clean_avatar(self):
        return validate_image(self.cleaned_data.get('avatar'))
