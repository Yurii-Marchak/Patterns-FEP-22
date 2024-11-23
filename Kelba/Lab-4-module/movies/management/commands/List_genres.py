from django.core.management.base import BaseCommand
from movies.models import Genre  

class Command(BaseCommand):
    help = 'Вивести всі жанри'

    def handle(self, *args, **kwargs):
        
        genres_info = Genre.objects.all()

        if genres_info.exists():
            for genre in genres_info:
                self.stdout.write(f"Name: {genre.name}")
                self.stdout.write('---')
        else:
            self.stdout.write("No genres found.")