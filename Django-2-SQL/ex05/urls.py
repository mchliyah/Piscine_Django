from django.urls import re_path

from .views import display, populate, remove

urlpatterns = [
    re_path(r"^ex05/populate/?$", populate, name="ex05-populate"),
    re_path(r"^ex05/display/?$", display, name="ex05-display"),
    re_path(r"^ex05/remove/?$", remove, name="ex05-remove"),
]
