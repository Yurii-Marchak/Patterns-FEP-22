from django import forms
from .models import Movie, Genre, Category

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'poster', 'year', 'country', 'directors', 'actors', 'genres', 'category']

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True
    )