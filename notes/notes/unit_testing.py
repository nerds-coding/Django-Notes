from django.test import TestCase
from django.contrib.auth.models import User
from all_notes.models import Note, NotesVersionControl


class NoteModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        self.note = Note.objects.create(owner=self.user)

    def test_add_shared_user(self):
        new_user = User.objects.create_user(
            username="newuser", email="new@example.com", password="password"
        )
        self.note.add_shared_user(new_user)
        self.assertIn(new_user, self.note.shared_with.all())


class NotesVersionControlModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        self.note = Note.objects.create(owner=self.user)
        self.version = NotesVersionControl.objects.create(
            title="Test Title",
            content="Test Content",
            note=self.note,
            updated_by=self.user,
        )

    def test_version_control_creation(self):
        self.assertEqual(self.version.title, "Test Title")
        self.assertEqual(self.version.content, "Test Content")
        self.assertEqual(self.version.note, self.note)
        self.assertEqual(self.version.updated_by, self.user)

    def test_version_control_ordering(self):
        version2 = NotesVersionControl.objects.create(
            title="Second Title",
            content="Second Content",
            note=self.note,
            updated_by=self.user,
        )
        versions = NotesVersionControl.objects.filter(note=self.note)
        self.assertEqual(versions[0], version2) 


