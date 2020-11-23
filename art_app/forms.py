from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    pronouns = forms.ChoiceField(
        choices=(
            (1, "they/them"),
            (2, "he/him"),
            (3, "she/her")
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "pronouns", "password1", "password2")