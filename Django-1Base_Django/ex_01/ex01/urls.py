from django.urls import path

from .views import display_page, django_page, template_engine_page

urlpatterns = [
    path("ex01/django", django_page, name="ex01-django"),
    path("ex01/display", display_page, name="ex01-display"),
    path("ex01/templates", template_engine_page, name="ex01-templates"),
    path("django_page", django_page, name="django-page-compat"),
]
