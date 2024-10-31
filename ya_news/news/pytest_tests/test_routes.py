from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


HOME_URL = pytest.lazy_fixture('home_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
ANON_CLIENT = pytest.lazy_fixture('client')
FROM_LOGIN_TO_EDIT_URL = pytest.lazy_fixture('from_login_to_edit_url')
FROM_LOGIN_TO_DELETE_URL = pytest.lazy_fixture('from_login_to_delete_url')


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status', (
        (HOME_URL, ANON_CLIENT, HTTPStatus.OK),
        (LOGIN_URL, ANON_CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, ANON_CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, ANON_CLIENT, HTTPStatus.OK),
        (DETAIL_URL, ANON_CLIENT, HTTPStatus.OK),
        (DELETE_URL, ANON_CLIENT, HTTPStatus.FOUND),
        (EDIT_URL, ANON_CLIENT, HTTPStatus.FOUND), (
            DELETE_URL,
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND
        ), (
            DELETE_URL,
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ), (
            EDIT_URL,
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND
        ), (
            EDIT_URL,
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK
        ),
    ),
)
def test_pages_availability(url, parametrized_client, expected_status):
    assert parametrized_client.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, redirect_url', (
        (EDIT_URL, FROM_LOGIN_TO_EDIT_URL),
        (DELETE_URL, FROM_LOGIN_TO_DELETE_URL)
    )
)
def test_redirects(client, url, redirect_url):
    assertRedirects(client.get(url), redirect_url)
