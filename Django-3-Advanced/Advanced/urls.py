"""
URL configuration for Advanced project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

from ex00 import views
from ex01 import views as ex01_views
from ex02 import views as ex02_views

urlpatterns = [
    path('set-language/', set_language, name='set_language'),
]

urlpatterns += i18n_patterns(
    # path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('articles/', views.ArticlesView.as_view(), name='articles'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('publications/', ex01_views.PublicationsView.as_view(), name='publications'),
    path('detail/<int:pk>/', ex01_views.DetailArticleView.as_view(), name='detail'),
    path('logout/', ex01_views.UserLogoutView.as_view(), name='logout'),
    path('favourites/', ex01_views.FavouritesView.as_view(), name='favourites'),
    path('register/', ex02_views.RegisterView.as_view(), name='register'),
    path('publish/', ex02_views.PublishView.as_view(), name='publish'),
    path('detail/<int:pk>/favourite/', ex02_views.AddFavouriteView.as_view(), name='add_favourite'),
)
