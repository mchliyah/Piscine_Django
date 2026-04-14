from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('', views.account_page, name='page'),
    path('login/', views.login_ajax, name='ajax_login'),
    path('logout/', views.logout_ajax, name='ajax_logout'),
]