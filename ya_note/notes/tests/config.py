from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase

from notes.models import Note


SLUG = 'slug'
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')
EDIT_URL = reverse('notes:edit', args=(SLUG,))
SUCCESS_URL = reverse('notes:success')
HOME_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
DETAIL_URL = reverse('notes:detail', args=(SLUG,))
DELETE_URL = reverse('notes:delete', args=(SLUG,))
FROM_LOGIN_TO_LIST_URL = f'{LOGIN_URL}?next={LIST_URL}'
FROM_LOGIN_TO_SUCCESS_URL = f'{LOGIN_URL}?next={SUCCESS_URL}'
FROM_LOGIN_TO_ADD_URL = f'{LOGIN_URL}?next={ADD_URL}'
FROM_LOGIN_TO_DETAIL_URL = f'{LOGIN_URL}?next={DETAIL_URL}'
FROM_LOGIN_TO_EDIT_URL = f'{LOGIN_URL}?next={EDIT_URL}'
FROM_LOGIN_TO_DELETE_URL = f'{LOGIN_URL}?next={DELETE_URL}'


User = get_user_model()


class Config(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author = User.objects.create(username='Читатель простой')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug=SLUG
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }
