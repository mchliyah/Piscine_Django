from django.urls import re_path

from .views import display_page, django_page, template_engine_page

urlpatterns = [
    re_path(r"^ex01/django/?$", django_page, name="ex01-django"),
    re_path(r"^ex01/display/?$", display_page, name="ex01-display"),
    re_path(r"^ex01/templates/?$", template_engine_page, name="ex01-templates"),
]
