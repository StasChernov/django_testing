from http import HTTPStatus

from notes.tests.constants import (
    SetUp,
    HOME_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
    LIST_URL,
    SUCCESS_URL,
    ADD_URL,
    DETAIL_URL,
    EDIT_URL,
    DELETE_URL
)


class TestRoutes(SetUp):

    def test_pages_availability(self):
        parametrizes = (
            (HOME_URL, self.client, HTTPStatus.OK),
            (LOGIN_URL, self.client, HTTPStatus.OK),
            (LOGOUT_URL, self.client, HTTPStatus.OK),
            (SIGNUP_URL, self.client, HTTPStatus.OK),
            (LIST_URL, self.author_client, HTTPStatus.OK),
            (SUCCESS_URL, self.author_client, HTTPStatus.OK),
            (ADD_URL, self.author_client, HTTPStatus.OK),
            (DETAIL_URL, self.author_client, HTTPStatus.OK),
            (EDIT_URL, self.author_client, HTTPStatus.OK),
            (DELETE_URL, self.author_client, HTTPStatus.OK),
            (DETAIL_URL, self.not_author_client, HTTPStatus.NOT_FOUND),
            (EDIT_URL, self.not_author_client, HTTPStatus.NOT_FOUND),
            (DELETE_URL, self.not_author_client, HTTPStatus.NOT_FOUND),
        )
        for (url, parametrize_client, status) in parametrizes:
            with self.subTest(
                url=url,
                client=parametrize_client,
                status=status
            ):
                self.assertEqual(
                    parametrize_client.get(url).status_code,
                    status
                )

    def test_redirect_for_anonymous_client(self):
        urls = (
            LIST_URL,
            SUCCESS_URL,
            ADD_URL,
            DETAIL_URL,
            EDIT_URL,
            DELETE_URL,
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    f'{LOGIN_URL}?next={url}'
                )
