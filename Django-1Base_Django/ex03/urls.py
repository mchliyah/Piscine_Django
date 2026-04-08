from django.urls import re_path

from .views import ex03_page

urlpatterns = [
    re_path(r"^ex03/?$", ex03_page, name="ex03-page"),
]
