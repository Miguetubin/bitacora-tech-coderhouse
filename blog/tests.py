from io import BytesIO
from tempfile import TemporaryDirectory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from PIL import Image
from .models import Post


def image_file(name='test.png'):
    output = BytesIO()
    Image.new('RGB', (20, 20), 'green').save(output, format='PNG')
    return SimpleUploadedFile(name, output.getvalue(), content_type='image/png')


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(username='autor', password='Prueba-Segura-731!')
        cls.other = get_user_model().objects.create_user(username='otro', password='Prueba-Segura-732!')
        cls.post = Post.objects.create(title='Aprender Python', content='Django y modelos', author=cls.owner)

    def setUp(self):
        self.media = TemporaryDirectory()
        self.settings_override = override_settings(MEDIA_ROOT=self.media.name)
        self.settings_override.enable()
        self.addCleanup(self.media.cleanup)
        self.addCleanup(self.settings_override.disable)

    def test_public_pages_and_missing_image(self):
        for url in ['/', '/acerca-de/', self.post.get_absolute_url()]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, '<img src=""')
        self.assertContains(self.client.get('/'), 'Aprender Python')
        self.assertEqual(self.client.get('/publicaciones/99999/').status_code, 404)

    def test_anonymous_routes_get_and_post_are_protected(self):
        urls = [reverse('blog:post_create'), reverse('blog:post_update', args=[self.post.pk]),
                reverse('blog:post_delete', args=[self.post.pk]), reverse('accounts:profile'),
                reverse('accounts:profile_edit')]
        for url in urls:
            for method in [self.client.get, self.client.post]:
                with self.subTest(url=url, method=method.__name__):
                    self.assertRedirects(method(url), f'/cuentas/login/?next={url}', fetch_redirect_response=False)
        self.assertEqual(Post.objects.count(), 1)

    def test_web_crud_with_image_and_clear(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'Nuevo artículo', 'content': 'Contenido real', 'category': 'web', 'image': image_file(),
            'author': self.other.pk,
        })
        post = Post.objects.get(title='Nuevo artículo')
        self.assertRedirects(response, post.get_absolute_url())
        self.assertEqual(post.author, self.owner)
        self.assertTrue(post.image.storage.exists(post.image.name))
        self.assertContains(self.client.get(post.get_absolute_url()), post.image.url)
        self.assertContains(self.client.get('/'), post.image.url)
        response = self.client.post(reverse('blog:post_update', args=[post.pk]), {
            'title': 'Título editado', 'content': 'Texto editado', 'category': 'python', 'image-clear': 'on',
        })
        self.assertRedirects(response, post.get_absolute_url())
        post.refresh_from_db()
        self.assertEqual(post.title, 'Título editado')
        self.assertFalse(post.image)
        self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 200)
        delete_url = reverse('blog:post_delete', args=[post.pk])
        self.assertEqual(self.client.get(delete_url).status_code, 200)
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())
        self.assertRedirects(self.client.post(delete_url), '/')
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_other_user_cannot_edit_or_delete(self):
        self.client.force_login(self.other)
        for name in ['blog:post_update', 'blog:post_delete']:
            for method in [self.client.get, self.client.post]:
                self.assertEqual(method(reverse(name, args=[self.post.pk])).status_code, 404)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Aprender Python')

    def test_validation_rejects_empty_and_fake_images(self):
        self.client.force_login(self.owner)
        url = reverse('blog:post_create')
        for data in [
            {'title': ' ', 'content': ' ', 'category': 'python'},
            {'title': 'Imagen falsa', 'content': 'Texto', 'category': 'python',
             'image': SimpleUploadedFile('falso.png', b'no es una imagen', content_type='image/png')},
        ]:
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
        self.assertEqual(Post.objects.count(), 1)

    def test_search_title_content_empty_and_no_results(self):
        self.assertContains(self.client.get('/', {'q': 'Python'}), 'Aprender Python')
        self.assertContains(self.client.get('/', {'q': 'modelos'}), 'Aprender Python')
        self.assertContains(self.client.get('/', {'q': 'imposiblexyz'}), 'No encontramos coincidencias')
        self.assertEqual(self.client.get('/', {'q': '  '}).context['page_obj'].paginator.count, 1)

    def test_pagination_preserves_search(self):
        Post.objects.bulk_create([Post(title=f'Python {i}', content='Ejemplo', author=self.owner) for i in range(7)])
        response = self.client.get('/', {'q': 'Python'})
        self.assertEqual(len(response.context['page_obj']), 6)
        self.assertContains(response, '?q=Python&amp;page=2')
        self.assertEqual(len(self.client.get('/', {'q': 'Python', 'page': 2}).context['page_obj']), 2)

    def test_csrf_required_on_write(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        self.assertEqual(client.post(reverse('blog:post_delete', args=[self.post.pk])).status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_template_escapes_content(self):
        self.post.content = '<script>alert("x")</script>'
        self.post.save()
        response = self.client.get(self.post.get_absolute_url())
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>')

    def test_demo_is_reproducible_without_password(self):
        call_command('seed_demo', verbosity=0, stdout=BytesIOText())
        count = Post.objects.count()
        call_command('seed_demo', verbosity=0, stdout=BytesIOText())
        self.assertEqual(Post.objects.count(), count)
        self.assertEqual(count, 4)
        author = get_user_model().objects.get(username='bitacora_demo')
        self.assertFalse(author.has_usable_password())
        self.assertEqual(Post.objects.exclude(image='').count(), 2)


class BytesIOText:
    def write(self, text):
        pass
