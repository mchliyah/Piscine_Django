from django import forms

class SearchForm(forms.Form):
    min_release_date = forms.DateField()
    max_release_date = forms.DateField()
    planet_diameter_gt = forms.IntegerField()
    gender = forms.ChoiceField()
