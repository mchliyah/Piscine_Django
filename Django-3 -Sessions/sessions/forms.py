from django import forms
from django.contrib.auth import get_user_model


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        user_model = get_user_model()
        if user_model.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already used.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        if password and password_confirmation and password != password_confirmation:
            self.add_error("password_confirmation", "Passwords must match exactly.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class TipForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Tip Content")
