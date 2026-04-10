from django.urls import re_path

from .views import display, init, populate, update

urlpatterns = [
    re_path(r"^ex06/init/?$", init, name="ex06-init"),
    re_path(r"^ex06/populate/?$", populate, name="ex06-populate"),
    re_path(r"^ex06/display/?$", display, name="ex06-display"),
    re_path(r"^ex06/update/?$", update, name="ex06-update"),
]
