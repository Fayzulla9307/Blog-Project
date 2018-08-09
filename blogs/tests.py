from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='fayzulla',
            email='fayzulla9307@mail.ru',
            password='secret'
        )

        cls.post = Post.objects.create(
            title='A good title',
            text='Nice text content',
            author=cls.user,
        )

    def setUp(self):
        self.post.refresh_from_db()

    def test_string_representation(self):
        post = Post(title='A sample title')

        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'fayzulla')
        self.assertEqual(f'{self.post.text}', 'Nice text content')

    def test_post_list_view(self):
        url = reverse('home')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice text content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
#        import pdb; pdb.set_trace()
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
        'title': 'New Title',
        'text': 'New Text',
        'author': self.user,
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Title')
        self.assertContains(response, 'New Text')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'text': 'Updated text',
        })

        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))

        self.assertEqual(response.status_code, 200)
