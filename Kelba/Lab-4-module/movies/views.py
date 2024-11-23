from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect, render
from movies.utils.movies import get_all_movies 
from movies.utils.genres import get_all_genres
from .models import Movie, Genre, Category
from .serializers import MovieSerializer
from .forms import MovieForm

def movies(request):
    """
    Головна сторінка з фільмами. Тільки GET.
    """
    movies_info = get_all_movies()  # Заміна get_all_movies() на виклик Movie.objects.all()
    genres = Genre.objects.all()  
    categories = Category.objects.all()  
    form = MovieForm()  
    return render(
        request, 
        'movies/main.html', 
        {
            'movies': movies_info,
            'genres': genres,
            'categories': categories,
            'form': form  
        }
    )

def add_movie(request):
    """
    Обробка додавання нового фільму через форму.
    """
    if request.method == 'POST':
        # Обробка даних форми
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            # Після успішного збереження перенаправляємо на головну сторінку
            return redirect('')  # Перенаправляємо на сторінку movies
    else:
        form = MovieForm()

    return render(request, 'movies/main.html', {'form': form})


class PublicMovieView(APIView):
    """
    Публічний доступ до фільмів (тільки GET).
    """
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminMovieView(APIView):
    """
    Адміністратор може робити повний CRUD для фільмів.
    """
    #permission_classes = [permissions.IsAdminUser]  # Тільки для адміністратора

    def get(self, request, pk=None):
        if pk:
            # Отримати конкретний фільм
            try:
                movie = Movie.objects.get(pk=pk)
            except Movie.DoesNotExist:
                return Response({"detail": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Отримати список усіх фільмів
            movies = Movie.objects.all()
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk is None:
            return Response({"detail": "Movie ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"detail": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

    
        serializer = MovieSerializer(movie, data=request.data, partial=False)  # partial=True для часткового оновлення
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
