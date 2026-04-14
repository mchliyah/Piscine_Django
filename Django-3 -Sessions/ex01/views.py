from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from sessions.forms import LoginForm, RegistrationForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        login(request, user)
        return redirect("home")

    return render(request, "registration.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(request, user)
            return redirect("home")
        form.add_error(None, "Wrong username/password.")

    return render(request, "login.html", {"form": form})


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("home")
