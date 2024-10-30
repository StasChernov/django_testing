import pytest


from datetime import datetime, timedelta
from django.conf import settings
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse
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
    note = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return note


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
def comment_text():
    return 'Текст комментария'


@pytest.fixture
def new_comment_text():
    return 'Обновлённый комментарий'


@pytest.fixture
def comment(author, news, comment_text):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=comment_text
    )
    return comment


@pytest.fixture
def form_data(comment_text):
    return {'text': comment_text}


@pytest.fixture
def new_form_data(new_comment_text):
    return {'text': new_comment_text}


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
    return news_url + '#comments'


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))
