# events/models.py
from django.db import models

class FootballEvent(models.Model):
    event_id = models.IntegerField(unique=True)
    tournament = models.CharField(max_length=100)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    start_timestamp = models.IntegerField()
    slug = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
