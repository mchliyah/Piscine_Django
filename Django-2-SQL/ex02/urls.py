from django.urls import re_path

from .views import init, populate, display

urlpatterns = [
    re_path(r"^ex02/init/?$", init, name="ex02-init"),
    re_path(r"^ex02/populate/?$", populate, name="ex02-populate"),
    re_path(r"^ex02/display/?$", display, name="ex02-display")
]
