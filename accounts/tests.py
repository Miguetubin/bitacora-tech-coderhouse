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

    def test_missing_avatar_has_fallback_and_profile_can_be_edited(self):
        profile = Profile.objects.create(user=self.user)
        profile.avatar.save('perdido.png', image_file(), save=True)
        missing_url = profile.avatar.url
        profile.avatar.storage.delete(profile.avatar.name)
        self.client.force_login(self.user)
        self.assertNotContains(self.client.get(reverse('accounts:profile')), missing_url)
        response = self.client.post(reverse('accounts:profile_edit'), {
            'first_name': 'Miguel', 'last_name': 'Tubin', 'email': 'test@example.com', 'bio': 'Sin archivo original',
        })
        self.assertRedirects(response, reverse('accounts:profile'))

    def test_invalid_profile_does_not_partially_save_user_data(self):
        profile = Profile.objects.create(user=self.user, bio='Biografía original')
        self.client.force_login(self.user)
        for email, bio in [('test@example.com', 'A' * 501), ('correo-invalido', 'Biografía nueva')]:
            response = self.client.post(reverse('accounts:profile_edit'), {
                'first_name': 'Cambio que no debe guardarse', 'last_name': 'Tubin', 'email': email, 'bio': bio,
            })
            self.assertEqual(response.status_code, 200)
            self.user.refresh_from_db()
            profile.refresh_from_db()
            self.assertEqual(self.user.first_name, '')
            self.assertEqual(profile.bio, 'Biografía original')

    def test_profile_cannot_escalate_privileges_or_modify_another_user(self):
        other = get_user_model().objects.create_user(username='otro')
        self.client.force_login(self.user)
        self.assertRedirects(self.client.post(reverse('accounts:profile_edit'), {
            'first_name': 'Miguel', 'last_name': 'Tubin', 'email': 'test@example.com', 'bio': 'Actualizado',
            'user': other.pk, 'id': other.pk, 'username': 'otro', 'is_staff': 'on', 'is_superuser': 'on',
        }), reverse('accounts:profile'))
        self.user.refresh_from_db()
        other.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertEqual(self.user.username, 'miguel')
        self.assertEqual(other.first_name, '')

    def test_registration_validation_and_authenticated_redirect(self):
        for data in [
            {},
            {'username': 'nuevo', 'email': 'invalido', 'password1': 'Segura-731!zz', 'password2': 'Segura-731!zz'},
            {'username': 'nuevo', 'email': 'nuevo@example.com', 'password1': 'Segura-731!zz', 'password2': 'Distinta-731!zz'},
        ]:
            response = self.client.post(reverse('accounts:register'), data)
            self.assertTrue(response.context['form'].errors)
            self.assertEqual(get_user_model().objects.count(), 1)
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get(reverse('accounts:register')), reverse('accounts:profile'))

    def test_csrf_is_required_on_all_forms(self):
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        for name in ['accounts:register', 'accounts:login']:
            self.assertEqual(client.post(reverse(name), {}).status_code, 403)
        client.force_login(self.user)
        post = Post.objects.create(title='Protegido', content='Texto', author=self.user)
        urls = [reverse('accounts:profile_edit'), reverse('accounts:logout'), reverse('blog:post_create'),
                reverse('blog:post_update', args=[post.pk]), reverse('blog:post_delete', args=[post.pk])]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(client.post(url, {}).status_code, 403)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())

    def test_avatar_size_and_invalid_format_are_rejected(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        self.client.force_login(self.user)
        large_image = image_file()
        for image in [
            SimpleUploadedFile('grande.png', large_image.read().ljust(5 * 1024 * 1024 + 1, b'\0'), content_type='image/png'),
            SimpleUploadedFile('falsa.png', b'no es una imagen', content_type='image/png'),
        ]:
            response = self.client.post(reverse('accounts:profile_edit'), {
                'first_name': 'No guardar', 'last_name': '', 'email': 'test@example.com', 'bio': '', 'avatar': image,
            })
            self.assertTrue(response.context['profile_form'].errors)
            self.user.refresh_from_db()
            self.assertEqual(self.user.first_name, '')

    def test_admin_panel_is_optional_and_requires_staff(self):
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get('/admin/'), '/admin/login/?next=/admin/')
        admin = get_user_model().objects.create_superuser(username='admin_prueba', email='admin@example.com', password='Admin-Prueba-731!')
        self.client.force_login(admin)
        for url in ['/admin/', '/admin/blog/post/', '/admin/accounts/profile/', '/admin/auth/user/']:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)
