from django.urls import include, path

urlpatterns = [
    path("", include("ex00.urls")),
    # path("", include("ex01.urls")),
    path("", include("ex02.urls")),
    path("", include("ex03.urls")),
    path("", include("ex04.urls")),
    path("", include("ex05.urls")),
    path('ex06/', include('ex06.urls')),
    path('ex07/', include('ex07.urls')),
    path('ex08/', include('ex08.urls')),
    path('ex09/', include('ex09.urls')),
    path('ex10/', include('ex10.urls')),
]
