from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Group, Post
from http import HTTPStatus

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create(username='user_author')
        cls.user_not_author = User.objects.create(username='user_not_author')
        cls.group = Group.objects.create(
            slug='test-slug',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user_author,
            group=cls.group
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

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user_author}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.post_author.get(url)
                self.assertTemplateUsed(response, template)

    def test_urls_status_code(self):
        urls_names = [
            ['/', self.guest_client, HTTPStatus.OK],
            ['/about/author/', self.guest_client, HTTPStatus.OK],
            ['/about/tech/', self.guest_client, HTTPStatus.OK],
            [f'/group/{self.group.slug}/', self.guest_client, HTTPStatus.OK],
            [f'/profile/{self.user_author}/', self.guest_client,
                HTTPStatus.OK],
            [f'/posts/{self.post.id}/', self.guest_client, HTTPStatus.OK],

            [f'/posts/{self.post.id}/edit/', self.post_author, HTTPStatus.OK],
            [f'/posts/{self.post.id}/edit/', self.guest_client,
                HTTPStatus.FOUND],

            ['/create/', self.authorized_client, HTTPStatus.OK],
            ['/create/', self.guest_client, HTTPStatus.FOUND],

            # Запрос к страница unixisting_page вернет ошибку 404
            ['/unixisting_page/', self.guest_client, HTTPStatus.NOT_FOUND],
        ]
        for url, client, status in urls_names:
            with self.subTest(url=url):
                self.assertEqual(client.get(url).status_code, status)

    # Проверяем редиректы для неавторизованного пользователя
    def test_post_edit_url_redirect_anonymous(self):
        """Страница /post_id/edit перенаправляет анонимного пользователя."""
        response = self.guest_client.get(f'/posts/{self.post.id}/edit/')
        self.assertRedirects(response, f'/auth/login/?next=/posts/'
                                       f'{self.post.id}/edit/')

    def test_post_create_url_redirect_anonymous(self):
        """Страница /posts/create/ перенаправляет анонимного пользователя. """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, ('/auth/login/?next=/create/'))
