from movies.models import Movie

def get_all_movies():
    """Функція для отримання та виведення всіх фільмів з бази даних."""
    movies = Movie.objects.all()

    if movies.exists():
        movies_info = []
        for movie in movies:
            movie_data = {
                'Id': movie.id,
                'Title': movie.title,
                'Description': movie.description,
                'Poster': movie.poster,
                'Year': movie.year,
                'Country': movie.country,
                'Director': movie.directors,
                'Actors': movie.actors,
                'Genres': ', '.join([genre.name for genre in movie.genres.all()]),
                'Category': movie.category.name if movie.category else "N/A",

            }
            movies_info.append(movie_data)
        return movies_info
    else:
        return "No movies found in the database."
    
    