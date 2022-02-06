from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()

INDEX = reverse('posts:main')
NEW_POST = reverse('posts:post_create')


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create(username='user_author')
        cls.user_not_author = User.objects.create(username='user_not_author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Тестовая группа2',
            slug='test-slug2',
            description='Тестовое описание2',
        )
        cls.post = Post.objects.create(
            author=cls.user_author,
            text='Текст поста',
            group=cls.group,
        )

    def setUp(self):
        # Неавторизованный клиент
        self.guest_client = Client()
        # Авторизованный клиент, не автор
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_not_author)
        # Автор
        self.post_author = Client()
        self.post_author.force_login(self.user_author)

    def test_post_create(self):
        post = Post.objects.first()
        post.delete()
        form_data = {
            'text': 'Текст формы',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        post = response.context['page_obj'][0]
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group, self.group)
        self.assertEqual(post.author, self.user_not_author)
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'user_not_author'})
        )

    def test_create_post_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом."""
        urls = [
            reverse('posts:post_create'),
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        ]
        for url in urls:
            response = self.authorized_client.get(url)
            form_fields = {
                'text': forms.fields.CharField,
                'group': forms.fields.Field,
            }
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context.get('form').fields.get(value)
                    self.assertIsInstance(form_field, expected)

    def test_post_edit_save(self):
        """Корректное отображение post_edit. """
        form_data = {
            'text': 'Другой текст!',
            'group': self.group2.id,
        }
        response = self.post_author.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data, follow=True
        )
        '''Пост должен поменяться'''
        post = response.context['post']
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group, self.group2)
        self.assertEqual(post.author, self.post.author)
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id})
        )
