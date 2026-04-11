from django.shortcuts import render
from .models import People, Movies
from .forms import SearchForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

@csrf_exempt
def search_view(request):
    results = None
    form = None
    
    genders = People.objects.values_list('gender', flat=True).distinct()
    gender_choices = [(g, g) for g in sorted(set(genders)) if g]
    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        form.fields['gender'].choices = gender_choices
        
        if form.is_valid():
            min_date = form.cleaned_data['min_release_date']
            max_date = form.cleaned_data['max_release_date']
            diameter = form.cleaned_data['planet_diameter_gt']
            gender = form.cleaned_data['gender']

            movies = Movies.objects.filter(
                release_date__range=(min_date, max_date)
            ).prefetch_related('characters__homeworld').distinct()

            results = []
            for movie in movies:
                matching_people = movie.characters.filter(
                    gender=gender,
                    homeworld__diameter__gte=diameter
                ).select_related('homeworld')
                
                for person in matching_people:
                    results.append({
                        'movie': movie,
                        'person': person
                    })
    else:
        form = SearchForm()
        form.fields['gender'].choices = gender_choices

    return render(request, 'ex10/search.html', {
        'form': form, 
        'results': results
    })
