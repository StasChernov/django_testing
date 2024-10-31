from http import HTTPStatus

from notes.tests.config import (
    Config,
    HOME_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
    LIST_URL,
    SUCCESS_URL,
    ADD_URL,
    DETAIL_URL,
    EDIT_URL,
    DELETE_URL,
    FROM_LOGIN_TO_LIST_URL,
    FROM_LOGIN_TO_SUCCESS_URL,
    FROM_LOGIN_TO_ADD_URL,
    FROM_LOGIN_TO_DETAIL_URL,
    FROM_LOGIN_TO_EDIT_URL,
    FROM_LOGIN_TO_DELETE_URL
)


class TestRoutes(Config):

    def test_pages_availability(self):
        parametrizes = (
            (HOME_URL, self.client, HTTPStatus.OK),
            (LOGIN_URL, self.client, HTTPStatus.OK),
            (LOGOUT_URL, self.client, HTTPStatus.OK),
            (SIGNUP_URL, self.client, HTTPStatus.OK),
            (LIST_URL, self.client, HTTPStatus.FOUND),
            (SUCCESS_URL, self.client, HTTPStatus.FOUND),
            (ADD_URL, self.client, HTTPStatus.FOUND),
            (DETAIL_URL, self.client, HTTPStatus.FOUND),
            (EDIT_URL, self.client, HTTPStatus.FOUND),
            (DELETE_URL, self.client, HTTPStatus.FOUND),
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
            (LIST_URL, FROM_LOGIN_TO_LIST_URL),
            (SUCCESS_URL, FROM_LOGIN_TO_SUCCESS_URL),
            (ADD_URL, FROM_LOGIN_TO_ADD_URL),
            (DETAIL_URL, FROM_LOGIN_TO_DETAIL_URL),
            (EDIT_URL, FROM_LOGIN_TO_EDIT_URL),
            (DELETE_URL, FROM_LOGIN_TO_DELETE_URL)
        )
        for (url, redirect_url) in urls:
            with self.subTest(url=url, redirect_url=redirect_url):
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url
                )
