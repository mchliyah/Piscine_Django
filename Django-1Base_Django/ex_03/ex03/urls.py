from django.urls import path

from .views import ex03_page

urlpatterns = [
    path("ex03", ex03_page, name="ex03-page"),
]
