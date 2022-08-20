from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="title"),
    path("notfound", views.not_found, name="notfound"),
    path("random", views.randompage, name="random"),
    path("newpage", views.create_page, name="newpage"),
    path("existing", views.existing_page, name="existing"),
    path("edit/<str:title>", views.edit, name="edit"),
]
