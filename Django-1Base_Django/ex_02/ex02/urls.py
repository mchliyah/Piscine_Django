from django.urls import path

from .views import ex02_page

urlpatterns = [
    path("ex02", ex02_page, name="ex02-page"),
]
