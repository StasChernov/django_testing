from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.config import (
    Config,
    ADD_URL,
    SUCCESS_URL,
    EDIT_URL,
    DELETE_URL,
    FROM_LOGIN_TO_ADD_URL
)


User = get_user_model()


class TestLogic(Config):

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        self.assertRedirects(
            self.client.post(ADD_URL, data=self.form_data),
            FROM_LOGIN_TO_ADD_URL
        )
        self.assertEqual(Note.objects.count(), 0)

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        response = self.author_client.post(ADD_URL, data=self.form_data)
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        Note.objects.all().delete()
        response = self.author_client.post(ADD_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        expected_slug = slugify(self.form_data['title'])
        note = Note.objects.get()
        self.assertEqual(note.slug, expected_slug)
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.author, self.author)

    def test_author_can_edit_note(self):
        response = self.author_client.post(EDIT_URL, self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_other_user_cant_edit_note(self):
        response = self.not_author_client.post(EDIT_URL, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)

    def test_author_can_delete_note(self):
        expected_count = Note.objects.count() - 1
        response = self.author_client.post(DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), expected_count)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_other_user_cant_delete_note(self):
        response = self.not_author_client.post(DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)
