from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .forms import LoginForm

def build_login_form(request, form=None):
	form = form or LoginForm(request)
	return render_to_string('account/_login_form.html', {'form': form}, request=request)


def build_logged_in_block(request):
	return render_to_string('account/_logged_in.html', {'user': request.user}, request=request)


@ensure_csrf_cookie
@require_GET
def account_page(request):
	context = {
		'login_form_html': build_login_form(request),
		'logged_in_html': build_logged_in_block(request),
	}
	return render(request, 'account/account.html', context)


@require_POST
def login_ajax(request):
	form = LoginForm(request, data=request.POST)
	if form.is_valid():
		user = form.get_user()
		login(request, user)
		return JsonResponse(
			{
				'success': True,
				'username': user.username,
				'logged_in_html': build_logged_in_block(request),
			}
		)

	return JsonResponse(
		{
			'success': False,
			'login_form_html': build_login_form(request, form),
		},
		status=400,
	)


@require_POST
def logout_ajax(request):
	logout(request)
	return JsonResponse(
		{
			'success': True,
			'login_form_html': build_login_form(request),
		}
	)
