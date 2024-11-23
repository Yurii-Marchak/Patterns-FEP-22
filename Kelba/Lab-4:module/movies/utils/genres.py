from movies.models import Genre

def get_all_genres():
    """Отримує всі жанри з бази даних."""
    return Genre.objects.all()