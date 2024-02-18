from django.contrib import admin
from all_notes.models import Note, NotesVersionControl

# Register your models here.


admin.site.register(Note)
admin.site.register(NotesVersionControl)
