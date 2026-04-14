from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy

from ex00.models import Article, UserFavouriteArticle


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)
        return response


class PublishView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'publish.html'
    fields = ['title', 'synopsis', 'content']
    success_url = reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddFavouriteView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    template_name = 'add_favourite.html'
    fields = ['article']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['article'].widget = forms.HiddenInput()
        form.fields['article'].initial = get_object_or_404(Article, pk=self.kwargs['pk'])
        return form

    def form_valid(self, form):
        article = form.cleaned_data['article']
        UserFavouriteArticle.objects.get_or_create(
            user=self.request.user,
            article=article,
        )
        return redirect('detail', pk=article.pk)



# subject:

# Using only CreateView, you must implement the following functionalities to your site.
# Each functionality must have its own URL:
# Register: HTML page featuring a ’POST’ type form allowing a logged out user to create
# a new user account.
# The form must require the login, a password and a password confirmation. this
# form must be accessible to a URL exclusively dedicated to it and ending with
# ’register’.
# Publish: HTML page featuring a ’POST’ type form allowing a logged-in user to publish
# a new article. The ’author’ field must not be displayed. It must be completed in
# the view during the validation process. You have to use a ’form’ object created
# by your view to generate your form (no handwritten <input> tag for the fields in
# your form!)
# Add a link towards this functionality in the Publications functionality template.
# Add to favourite: HTML page containing a ’POST’ type form located in the detail page
# of an article. No field must be visible. The ’article’ field must be pre-filled
# with the current article ID and during validation, ’user’ field must be filled with
# the logged user ID. This mechanism allows to add the current article in the logged
# user’s favorite list.
# No css formatting is required in this exercise.
# Did you know that Django proposes ready-made forms?