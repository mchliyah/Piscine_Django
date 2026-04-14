from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views.generic import DetailView, ListView, RedirectView

from ex00.models import Article


class PublicationsView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'publications.html'
    context_object_name = 'articles'
    queryset = Article.objects.select_related('author').all().order_by('-created')

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)


class DetailArticleView(DetailView):
    model = Article
    template_name = 'detail.html'
    context_object_name = 'article'


class UserLogoutView(LoginRequiredMixin, RedirectView):
    pattern_name = 'home'
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class FavouritesView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'favourites.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(
            userfavouritearticle__user=self.request.user
        ).select_related('author').order_by('-created').distinct()





#subject:
# Using only generic views (except ’View’ that you can’t inherit directly), you must
# implement the following functionalities to your site. Each functionality must have its
# own URL:
# Publications: HTML page displaying as HTML tables the fields ’title’, ’synopsis’ and
# ’created’, of every article recorded in the ’Article’ model whose user is currently logged-in.
# For each article, you also must implement a link which URL must include the article’s identification leading to the ’Detail’ functionality of said article.
# The table must have a ’header’ indicating the title of each column.
# Detail: HTML page displaying every field of a given article located in the database. It
# identification must be in the URL.
# Field disposition is free.
# For each article in the Articles functionality present in the HTML table from the
# previous exercise you will also add a link towards this article’s ’Detail’.
# Logout: A link logging out a logged in user. You can place the link wherever you want
# as long as it is visible and accessible. Once logged out, the user is redirected towards
# ’Home’.
# Favourites: HTML page displaying the titles of the current user’s favorite articles as a
# list of links.
# Each link - the URL of which must include the article’s identification - must lead
# to the article’s ’Detail’ functionality.
# You must provide at least one user with at least two different favorite articles.