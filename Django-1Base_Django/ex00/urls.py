from django.urls import re_path

from .views import markdown_cheatsheet

urlpatterns = [
    re_path(r"^ex00/?$", markdown_cheatsheet, name="ex00-markdown-cheatsheet"),
]
