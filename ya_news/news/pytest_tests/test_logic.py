from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError
import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


FORM_DATA = {
    'text': 'Текст комментария'
}
NEW_FORM_DATA = {
    'text': 'Обновлеленный комментарий'
}


bad_texts = [{
    'text': f'Какой-то текст, {bad_word}, еще текст'
} for bad_word in BAD_WORDS]
pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, detail_url):
    client.post(detail_url, data=FORM_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
    author,
    news,
    author_client,
    detail_url,
    url_to_comments
):
    response = author_client.post(detail_url, data=FORM_DATA)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
    'bad_texts',
    bad_texts
)
def test_user_cant_use_bad_words(author_client, detail_url, bad_texts):
    response = author_client.post(
        detail_url,
        data=bad_texts
    )
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, delete_url, url_to_comments):
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    not_author_client,
    delete_url,
    comment,
):
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1
    assert comment in Comment.objects.all()


def test_author_can_edit_comment(
    author_client,
    edit_url,
    url_to_comments,
    comment,
):
    response = author_client.post(edit_url, data=NEW_FORM_DATA)
    assertRedirects(response, url_to_comments)
    comment = Comment.objects.get(id=comment.id)
    assert comment.text == NEW_FORM_DATA['text']


def test_user_cant_edit_comment_of_another_user(
    not_author_client,
    edit_url,
    comment,
):
    response = not_author_client.post(edit_url, data=NEW_FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.get(id=comment.id)
    assert comment.text == FORM_DATA['text']
