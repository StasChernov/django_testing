from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.constants import (
    SetUp,
    ADD_URL,
    SUCCESS_URL,
    LOGIN_URL,
    EDIT_URL,
    DELETE_URL,
)


User = get_user_model()


class TestLogic(SetUp):

    def test_user_can_create_note(self):
        note_count_before_add = Note.objects.count()
        response = self.author_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), note_count_before_add + 1)
        new_note = Note.objects.last()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        note_count_before_add = Note.objects.count()
        self.assertRedirects(
            self.client.post(ADD_URL, data=self.form_data),
            f'{LOGIN_URL}?next={ADD_URL}'
        )
        self.assertEqual(Note.objects.count(), note_count_before_add)

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        note_count_before_add = Note.objects.count()
        response = self.author_client.post(ADD_URL, data=self.form_data)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), note_count_before_add)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        note_count_before_add = Note.objects.count()
        response = self.author_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), note_count_before_add + 1)
        expected_slug = slugify(self.form_data['title'])
        new_note = Note.objects.last()
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.author, self.author)

    def test_author_can_edit_note(self):
        response = self.author_client.post(EDIT_URL, self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.note = Note.objects.get()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])
        self.assertEqual(self.note.author, self.author)

    def test_other_user_cant_edit_note(self):
        response = self.not_author_client.post(EDIT_URL, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        note_count_before_delete = Note.objects.count()
        response = self.author_client.post(DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), note_count_before_delete - 1)

    def test_other_user_cant_delete_note(self):
        note_count_before_delete = Note.objects.count()
        response = self.not_author_client.post(DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), note_count_before_delete)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)
