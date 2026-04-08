from django import forms


class InputHistoryForm(forms.Form):
    text = forms.CharField(label="Text", max_length=1000)
