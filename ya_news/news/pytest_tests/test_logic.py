from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError
import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


NEW_FORM_DATA = {
    'text': 'Обновлеленный комментарий'
}


bad_texts = [{
    'text': f'Какой-то текст, {bad_word}, еще текст'
} for bad_word in BAD_WORDS]
pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(
    client,
    detail_url,
    comment
):
    Comment.objects.all().delete()
    client.post(detail_url, data={'text': comment.text})
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
    author,
    news,
    author_client,
    detail_url,
    url_to_comments,
    comment
):
    Comment.objects.all().delete()
    response = author_client.post(detail_url, data={'text': comment.text})
    assertRedirects(response, url_to_comments)
    assert Comment.objects.count() == 1
    comment_from_db = Comment.objects.get()
    assert comment_from_db.text == comment.text
    assert comment_from_db.news == comment.news
    assert comment_from_db.author == comment.author


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
    assert Comment.objects.count() == 1
    assert Comment.objects.filter(id=comment.id).exists() is True


def test_author_can_edit_comment(
    author_client,
    edit_url,
    url_to_comments,
    comment,
):
    response = author_client.post(edit_url, data=NEW_FORM_DATA)
    assertRedirects(response, url_to_comments)
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == NEW_FORM_DATA['text']
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_user_cant_edit_comment_of_another_user(
    not_author_client,
    edit_url,
    comment,
):
    response = not_author_client.post(edit_url, data=NEW_FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news
