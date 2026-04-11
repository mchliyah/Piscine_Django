from django.urls import re_path
from .views import init, populate, display

urlpatterns = [
    re_path(r"^ex08/init/?$", init, name='init'),
    re_path(r"^ex08/populate/?$",  populate, name='populate'),
    re_path(r"^ex08/display/?$",  display, name='display'),
]
