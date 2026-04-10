from django.shortcuts import render
from .models import People, Movies
from .forms import SearchForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def search_view(request):
    results = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            min_date = form.cleaned_data['min_release_date']
            max_date = form.cleaned_data['max_release_date']
            diameter = form.cleaned_data['planet_diameter_gt']
            gender = form.cleaned_data['gender']

            results = Movies.objects.filter(
                release_date__range=(min_date, max_date),
                characters__gender=gender,
                characters__homeworld__diameter__gte=diameter
            ).prefetch_related('characters').distinct()

    genders = People.objects.values_list('gender', flat=True).distinct()
    form = SearchForm(initial={'gender': genders})
    form.fields['gender'].choices = [(g, g) for g in genders]

    return render(request, 'ex10/search.html', {'form': form, 'results': results, 'gender_query': request.POST.get('gender')})
