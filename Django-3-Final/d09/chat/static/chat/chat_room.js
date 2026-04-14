(function ($) {
  function appendMessage(payload) {
    const messages = $('#messages');
    const username = payload.username || 'system';
    const content = payload.content || '';

    const line = payload.is_system
      ? `<div class="mb-2"><span class="badge text-bg-secondary me-2">system</span><span>${$('<div>').text(content).html()}</span></div>`
      : `<div class="mb-2"><strong>${$('<div>').text(username).html()}:</strong> <span>${$('<div>').text(content).html()}</span></div>`;

    messages.append(line);
    messages.scrollTop(messages[0].scrollHeight);
  }

  function connectSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const slug = window.chatRoomSlug;
    const socketUrl = `${protocol}://${window.location.host}/ws/chat/${slug}/`;
    const socket = new WebSocket(socketUrl);

    socket.onmessage = function (event) {
      const payload = JSON.parse(event.data);
      appendMessage(payload);
    };

    socket.onclose = function () {
      appendMessage({ username: 'system', content: 'Connection closed.', is_system: true });
    };

    $('#chat-form').on('submit', function (event) {
      event.preventDefault();
      const input = $('#chat-input');
      const message = input.val().trim();
      if (!message || socket.readyState !== WebSocket.OPEN) {
        return;
      }

      socket.send(JSON.stringify({ message: message }));
      input.val('');
    });

    const messages = $('#messages');
    if (messages.length) {
      messages.scrollTop(messages[0].scrollHeight);
    }
  }

  $(connectSocket);
})(jQuery);
