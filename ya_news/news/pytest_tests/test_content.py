from django.conf import settings
import pytest

from news.forms import CommentForm


pytestmark = pytest.mark.django_db


def test_news_count(all_news, client, home_url):
    response = client.get(home_url)
    news_count = response.context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(all_news, client, home_url):
    response = client.get(home_url)
    all_dates = [news.date for news in response.context['object_list']]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, comments, news, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, detail_url):
    assert 'form' not in client.get(detail_url).context


def test_authorized_client_has_form(author_client, detail_url):
    assert isinstance(
        author_client.get(detail_url).context.get('form'),
        CommentForm
    )
