from datetime import datetime, timedelta

from django.conf import settings
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse
import pytest

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comments(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def delete_url(news, comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def url_to_comment(news, comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def news_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_to_comments(news_url):
    return f'{news_url}#comments'


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def from_login_to_edit_url(login_url, edit_url):
    return f'{login_url}?next={edit_url}'


@pytest.fixture
def from_login_to_delete_url(login_url, delete_url):
    return f'{login_url}?next={delete_url}'
