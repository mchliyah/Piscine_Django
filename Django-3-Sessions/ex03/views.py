from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

from ex02.models import Tip


@login_required(login_url="login")
def upvote_tip(request, tip_id):
	if request.method != "POST":
		return redirect("home")

	tip = get_object_or_404(Tip, id=tip_id)
	user = request.user

	if tip.upvoters.filter(id=user.id).exists():
		tip.upvoters.remove(user)
	else:
		tip.downvoters.remove(user)
		tip.upvoters.add(user)

	return redirect("home")


@login_required(login_url="login")
def downvote_tip(request, tip_id):
    if request.method != "POST":
        return redirect("home")

    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user

    if not user.can_downvote_tip(tip):
        return HttpResponseForbidden("You are not allowed to downvote this tip.")

    if tip.downvoters.filter(id=user.id).exists():
        tip.downvoters.remove(user)
    else:
        tip.upvoters.remove(user)
        tip.downvoters.add(user)

    return redirect("home")


@login_required(login_url="login")
def delete_tip(request, tip_id):
    if request.method != "POST":
        return redirect("home")

    tip = get_object_or_404(Tip, id=tip_id)

    if not request.user.can_delete_tip(tip):
        return HttpResponseForbidden("You are not allowed to delete this tip.")

    tip.delete()
    return redirect("home")
