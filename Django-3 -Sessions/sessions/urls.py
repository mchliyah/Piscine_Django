from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ex00/", include("ex00.urls")),
    path("", include("ex01.urls")),
    path("", include("ex02.urls")),
    path("", include("ex03.urls")),
]
