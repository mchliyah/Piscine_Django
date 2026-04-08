from django.urls import re_path

from .views import init

urlpatterns = [
    re_path(r"^ex00/init/?$", init, name="ex00-init"),
]
