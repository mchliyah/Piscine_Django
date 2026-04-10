from django.urls import re_path

from .views import display, populate

urlpatterns = [
    re_path(r"^ex03/populate/?$", populate, name="ex03-populate"),
    re_path(r"^ex03/display/?$", display, name="ex03-display"),
]
