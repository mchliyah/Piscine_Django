from django.urls import re_path

from .views import ex02_page

urlpatterns = [
    re_path(r"^ex02/?$", ex02_page, name="ex02-page"),
]
