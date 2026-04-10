from django.urls import re_path

from .views import display, populate, update

urlpatterns = [
    re_path(r"^ex07/populate/?$", populate, name="ex07-populate"),
    re_path(r"^ex07/display/?$", display, name="ex07-display"),
    re_path(r"^ex07/update/?$", update, name="ex07-update"),
]
