from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from blog.tests import image_file
from blog.models import Post
from .models import Profile
from tempfile import TemporaryDirectory
from django.test import override_settings


class AccountsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='miguel', email='test@example.com', password='Prueba-Segura-731!')
        self.media = TemporaryDirectory()
        override = override_settings(MEDIA_ROOT=self.media.name)
        override.enable()
        self.addCleanup(self.media.cleanup)
        self.addCleanup(override.disable)

    def test_register_creates_account_profile_and_session(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'nuevo', 'email': 'nuevo@example.com', 'first_name': 'Nuevo',
            'last_name': 'Autor', 'password1': 'Otra-Segura-731!', 'password2': 'Otra-Segura-731!',
        })
        self.assertRedirects(response, '/')
        user = get_user_model().objects.get(username='nuevo')
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_register_rejects_duplicate_and_weak_password(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'miguel', 'email': 'nuevo@example.com', 'password1': '123', 'password2': '123',
        })
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_login_errors_login_next_and_post_logout(self):
        response = self.client.post(reverse('accounts:login'), {'username': 'miguel', 'password': 'incorrecta'})
        self.assertContains(response, 'form-errors')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'miguel', 'password': 'Prueba-Segura-731!', 'next': '/publicaciones/nueva/',
        })
        self.assertRedirects(response, '/publicaciones/nueva/')
        self.assertEqual(self.client.get(reverse('accounts:logout')).status_code, 405)
        self.assertRedirects(self.client.post(reverse('accounts:logout')), '/')
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(self.client.get(reverse('accounts:profile')), '/cuentas/login/?next=/cuentas/perfil/')

    def test_login_rejects_external_next(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'miguel', 'password': 'Prueba-Segura-731!', 'next': 'https://example.com/',
        })
        self.assertRedirects(response, '/')

    def test_profile_edit_avatar_clear_and_own_posts(self):
        self.client.force_login(self.user)
        self.assertContains(self.client.get(reverse('accounts:profile')), 'M')
        response = self.client.post(reverse('accounts:profile_edit'), {
            'first_name': 'Miguel', 'last_name': 'Tubin', 'email': 'test@example.com',
            'bio': 'Aprendiendo Python', 'avatar': image_file('avatar.png'),
        })
        self.assertRedirects(response, reverse('accounts:profile'))
        profile = Profile.objects.get(user=self.user)
        self.assertTrue(profile.avatar.storage.exists(profile.avatar.name))
        self.assertContains(self.client.get(reverse('accounts:profile')), profile.avatar.url)
        response = self.client.post(reverse('accounts:profile_edit'), {
            'first_name': 'Miguel', 'last_name': 'Tubin', 'email': 'test@example.com',
            'bio': 'Aprendiendo Python', 'avatar-clear': 'on',
        })
        self.assertEqual(response.status_code, 302)
        profile.refresh_from_db()
        self.assertFalse(profile.avatar)
        other = get_user_model().objects.create_user(username='otro')
        Post.objects.create(title='Publicación ajena', content='Texto', author=other)
        self.assertNotContains(self.client.get(reverse('accounts:profile')), 'Publicación ajena')

    def test_anonymous_and_authenticated_navigation(self):
        response = self.client.get('/')
        self.assertContains(response, 'Crear cuenta')
        self.assertNotContains(response, 'Mi perfil')
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertContains(response, 'Mi perfil')
        self.assertContains(response, 'Salir')
        self.assertNotContains(response, 'Crear cuenta')
