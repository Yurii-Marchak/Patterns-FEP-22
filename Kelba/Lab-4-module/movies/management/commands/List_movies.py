from django.core.management.base import BaseCommand
from movies.models import Movie, Genre  

class Command(BaseCommand):
    help = 'Вивести всі фільми'

    def handle(self, *args, **kwargs):
        
        movies_info = Movie.objects.all()

        
        if movies_info.exists():  
            for movie in movies_info:
                self.stdout.write(f"Title: {movie.title}")
                self.stdout.write(f"Description: {movie.description if movie.description else 'No description available'}")
                self.stdout.write(f"Poster: {movie.poster if movie.poster else 'No poster available'}")
                self.stdout.write(f"Year: {movie.year if movie.year else 'No year available'}")
                self.stdout.write(f"Country: {movie.country if movie.country else 'No country available'}")
                self.stdout.write(f"Directors: {movie.directors if movie.directors else 'No directors available'}")
                self.stdout.write(f"Actors: {movie.actors if movie.actors else 'No actors available'}")
                self.stdout.write(f"Genres: {', '.join([genre.name for genre in movie.genres.all()]) if movie.genres.exists() else 'No genres available'}")
                self.stdout.write(f"Category: {movie.category.name if movie.category else 'None'}")
                self.stdout.write('---')
        else:
            self.stdout.write("No movies found.")

