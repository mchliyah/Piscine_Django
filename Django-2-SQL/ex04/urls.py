from django.urls import re_path

from .views import display, init, populate, remove

urlpatterns = [
    re_path(r"^ex04/init/?$", init, name="ex04-init"),
    re_path(r"^ex04/populate/?$", populate, name="ex04-populate"),
    re_path(r"^ex04/display/?$", display, name="ex04-display"),
    re_path(r"^ex04/remove/?$", remove, name="ex04-remove"),
]
