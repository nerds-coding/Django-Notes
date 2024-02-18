from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:id>', views.get_notes_data),
    path('create', views.create_new_note),
    path('share', views.add_user_to_notes),
    path('version-history/<int:id>', views.notes_history),
]
