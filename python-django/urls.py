from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r"^notes/$", views.notes, name="notes"),
    re_path(r"^notes/(?P<index>\d+)/$", views.note_detail, name="note-detail"),
]
