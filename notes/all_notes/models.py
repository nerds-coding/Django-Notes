from django.db import models
from django.contrib.auth.admin import User

# Create your models here.

class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_owner')
    shared_with = models.ManyToManyField(User, related_name='shared_notes_with', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def add_shared_user(self, user):
        self.shared_with.add(user)

class NotesVersionControl(models.Model):
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='version_control')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by')
    
    class Meta:
        ordering = ['-timestamp']