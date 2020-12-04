from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Artwork, Collection


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


class ArtworkForm(forms.ModelForm):
    """Form to submit a new Artwork."""
    tags = forms.CharField(help_text="Enter a comma-separated list of tags.")

    class Meta:
        model = Artwork
        fields = ("image", "title", "caption")


class CollectionForm(forms.ModelForm):
    tags = forms.CharField(help_text="Enter a comma-separated list of tags.")
    class Meta:
        model = Collection
        fields = ("name",)
