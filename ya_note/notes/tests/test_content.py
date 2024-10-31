from notes.forms import NoteForm
from notes.tests.config import LIST_URL, ADD_URL, EDIT_URL, Config


class TestRoutes(Config):

    def test_note_in_list_for_author(self):
        response = self.author_client.get(LIST_URL)
        note_from_context = response.context['object_list'].get(
            id=self.note.id
        )
        self.assertIn(self.note, response.context['object_list'])
        self.assertEqual(note_from_context.slug, self.note.slug)
        self.assertEqual(note_from_context.text, self.note.text)
        self.assertEqual(note_from_context.title, self.note.title)
        self.assertEqual(note_from_context.author, self.note.author)

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
