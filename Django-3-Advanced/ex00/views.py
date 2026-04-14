from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView

from ex00.models import Article

# Once all of this is done, we can tackle the real goal of this first exercise.
# Using only generic views (except ’View’ that you can’t inherit directly), you must
# implement the following functionalities to your site. Each functionality must have its
# own URL:
# Articles: HTML page displaying every field as an HTML table (except the content) of
# every recorded article in the Article table).
# The table must have a header indicating the title of each column.
# Home: Mandatory URL: ’127.0.0.1:8000’. Redirects to Articles
# Login: HTML page displaying a POST type form. Logs an logged-out user thanks to a
# username and a password. In case of an error, the page must display a message
# describing said error. If successful, the view must redirect to ’Home’.
# You must also provide at least five articles examples from three different users. Provide
# fixtures if necessary. The article’s content doesn’t matter. Basic ’lorem ipsum’ can be
# enough.

class HomeView(RedirectView):
    pattern_name = 'articles'
    permanent = False


class ArticlesView(ListView):
    model = Article
    template_name = 'articles.html'
    context_object_name = 'articles'
    queryset = Article.objects.select_related('author').all().order_by('-created')

class UserLoginView(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')
    redirect_authenticated_user = True