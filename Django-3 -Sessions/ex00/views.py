from django.shortcuts import render
import random
from django.conf import settings
import time


def get_display_name(request):
    if request.user.is_authenticated:
        return f"{request.user.username} [{request.user.reputation}]"

    has_name = "user_name" in request.session
    has_timestamp = "timestamp" in request.session
    is_expired = has_timestamp and (time.time() - request.session["timestamp"] > 42)

    if (not has_name) or (not has_timestamp) or is_expired:
        request.session["user_name"] = random.choice(settings.USER_NAMES)
        request.session["timestamp"] = time.time()

    return request.session["user_name"]


def index(request):
    display_name = get_display_name(request)
    return render(request, "index.html", {"display_name": display_name, "tips": [], "tip_form": None})
