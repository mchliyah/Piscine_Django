(function ($) {
  function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(';') : [];

    for (let index = 0; index < cookies.length; index += 1) {
      const cookie = cookies[index].trim();
      console.log(`Checking cookie: ${cookie}`);
      if (cookie.substring(0, name.length + 1) === `${name}=`) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }

    return null;
  }

  function showFeedback(message, type) {
    const feedback = $('#account-feedback');
    feedback.empty();

    if (!message) {
      return;
    }

    feedback.html(`<div class="alert alert-${type} mb-0">${message}</div>`);
  }

  function refreshState(response) {
    if (response.logged_in_html) {
      $('#account-container').html(response.logged_in_html);
    }
    if (response.login_form_html) {
      $('#account-container').html(response.login_form_html);
    }
  }

  $(document).on('submit', '#login-form', function (event) {
    event.preventDefault();

    const loginUrl = $('#account-container').data('login-url');
    const formData = $(this).serialize();

    $.ajax({
      url: loginUrl,
      method: 'POST',
      data: formData,
      dataType: 'json',
      success(response) {
        showFeedback(`Welcome, ${response.username}.`, 'success');
        refreshState(response);
      },
      error(xhr) {
        const response = xhr.responseJSON;
        if (response && response.login_form_html) {
          showFeedback('Please fix the highlighted errors.', 'danger');
          refreshState(response);
          return;
        }

        showFeedback('Login failed. Please try again.', 'danger');
      },
    });
  });

  $(document).on('click', '#logout-button', function () {
    const logoutUrl = $('#account-container').data('logout-url');

    $.ajax({
      url: logoutUrl,
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      dataType: 'json',
      success(response) {
        showFeedback('You have been logged out.', 'info');
        refreshState(response);
      },
      error() {
        showFeedback('Logout failed. Please try again.', 'danger');
      },
    });
  });
})(jQuery);