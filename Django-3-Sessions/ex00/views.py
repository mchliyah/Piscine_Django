from django.shortcuts import render
import random
from django.conf import settings
import time

def index(request):
    if 'user_name' not in request.session or 'timestamp' not in request.session or time.time() - request.session['timestamp'] > 42:
        request.session['user_name'] = random.choice(settings.USER_NAMES)
        request.session['timestamp'] = time.time()
    
    user_name = request.session['user_name']
    return render(request, 'index.html', {'user_name': user_name})
