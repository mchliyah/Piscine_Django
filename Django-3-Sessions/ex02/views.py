from django.shortcuts import render

from ex00.views import get_display_name

from .forms import TipForm
from .models import Tip


def home_view(request):
    display_name = get_display_name(request)

    if request.method == "POST" and request.user.is_authenticated:
        tip_form = TipForm(request.POST)
        if tip_form.is_valid():
            tip = tip_form.save(commit=False)
            tip.author = request.user
            tip.save()
            tip_form = TipForm()
    else:
        tip_form = TipForm()

    tips = Tip.objects.select_related("author").prefetch_related("upvoters", "downvoters").order_by("-tip_date")

    if request.user.is_authenticated:
        for tip in tips:
            tip.can_downvote = request.user.can_downvote_tip(tip)
            tip.can_delete = request.user.can_delete_tip(tip)
    else:
        for tip in tips:
            tip.can_downvote = False
            tip.can_delete = False

    return render(
        request,
        "index.html",
        {
            "display_name": display_name,
            "tip_form": tip_form,
            "tips": tips,
        },
    )
