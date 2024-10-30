from notes.forms import NoteForm
from notes.tests.constants import LIST_URL, ADD_URL, EDIT_URL, SetUp


class TestRoutes(SetUp):

    def test_note_in_list_for_author(self):
        response = self.author_client.get(LIST_URL)
        self.assertIn(self.note, response.context['object_list'])

    def test_note_not_in_list_for_another_user(self):
        response = self.not_author_client.get(LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_pages_contains_form(self):
        urls = (
            ADD_URL,
            EDIT_URL
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
