# events/forms.py
from django import forms
from .models import FootballEvent

class FootballEventForm(forms.ModelForm):
    class Meta:
        model = FootballEvent
        fields = ['tournament', 'home_team', 'away_team', 'home_score', 'away_score', 'start_timestamp', 'slug']
