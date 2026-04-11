from django.urls import path
from . import views

urlpatterns = [
    path('ex10/', views.search_view, name='ex10_search'),
]
