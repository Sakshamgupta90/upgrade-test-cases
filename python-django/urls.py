from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^notes/$", views.notes, name="notes"),
    url(r"^notes/(?P<index>\d+)/$", views.note_detail, name="note-detail"),
]
