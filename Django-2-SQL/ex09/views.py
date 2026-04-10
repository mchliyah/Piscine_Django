from django.shortcuts import render
from .models import People, Planets
from django.db.models import Q

def display(request):
    try:
        people = People.objects.filter(
            Q(homeworld__climate__icontains='windy')
        ).order_by('name')

        if people.exists():
            return render(request, 'ex09/display.html', {'people': people})
        else:
            command = "python3 manage.py loaddata ex09_initial_data.json"
            return render(request, 'ex09/display.html', {'command': command})
    except Exception as e:
        command = "python3 manage.py loaddata ex09_initial_data.json"
        return render(request, 'ex09/display.html', {'command': command, 'error': str(e)})
