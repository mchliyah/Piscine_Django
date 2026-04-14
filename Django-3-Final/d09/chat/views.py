from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import ChatMessage, ChatRoom


@login_required
def room_list(request):
	rooms = ChatRoom.objects.order_by('id')
	context = {'rooms': rooms}
	return render(request, 'chat/room_list.html', context)


@login_required
def room_detail(request, slug):
	room = get_object_or_404(ChatRoom, slug=slug)
	messages = ChatMessage.objects.filter(room=room).select_related('user')
	context = {
		'room': room,
		'messages': messages,
	}
	return render(request, 'chat/room_detail.html', context)




# In this application, you must create a page displaying 3 links. Each of them must
# lead to a different ’chatrooms’.
# The names of these rooms must be in database. You must create a suitable model.
# Each of these links must lead to another page containing a standard functional chat.
# Each chat must have the following specification:
# • It must use ’jquery’ as sole frontend library as well as the Websockets to communicate with the server.(no AJAX)
# • It’s only available to connected users.
# • The name of the chat must appear somewhere.
# • Several users must be able to connect (just in case...).
# • A user can post a message (you had guessed, right?).
# • A message sent by a user must be visible by all the users who have joined the chatroom (everyone knows what a chatroom is, right? Haven’t you read that preamble?).
# • Messages must appear in the bottom and be displayed in ascending order (that
# one’s for you, by the heater, right.), along with the name of the user that posted
# them.
# 7
# Training Python-Django - 3 Final
# • Messages must not disappear. A message must not replace a previous one. The
# messages order must not change.
# • When a user joins the chatroom, the message ’<username> has joined the chat’
# must appear for all users to see, including the one who just joined. <username> is
# replaced by said user’s name of course.