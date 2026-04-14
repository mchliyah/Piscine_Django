# AJAX Study Notes

Use these references when you come back to the exercise later:

- MDN Ajax glossary: https://developer.mozilla.org/en-US/docs/Glossary/AJAX
- MDN network requests: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Network_requests
- jQuery AJAX API: https://api.jquery.com/jquery.ajax/
- Django forms guide: https://docs.djangoproject.com/en/5.2/topics/forms/
- Django authentication: https://docs.djangoproject.com/en/5.2/topics/auth/default/
- Django CSRF protection: https://docs.djangoproject.com/en/5.2/ref/csrf/

## What to remember

- AJAX means updating part of a page without a full reload.
- For this exercise, login and logout must be sent as AJAX `POST` requests.
- Django needs a CSRF token on unsafe requests like `POST`.
- `AuthenticationForm` handles login validation for you.
- `request.user.is_authenticated` decides what the page should show after refresh.

## Study order

1. Read the MDN Ajax glossary.
2. Read the MDN network requests article.
3. Read `jQuery.ajax()`.
4. Read Django forms.
5. Read Django authentication.
6. Read Django CSRF protection.

## Exercise flow

- Anonymous user: show login form.
- Valid login: replace the form with `Logged as <user>` and a logout button.
- Invalid login: keep the form and show errors on the page.
- Logged-in user refresh: render the logged-in state again from Django.
- Logout: remove the logged-in state and show the form again.