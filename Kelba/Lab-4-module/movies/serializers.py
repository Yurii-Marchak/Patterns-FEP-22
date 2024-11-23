from rest_framework import serializers
from .models import Category, Genre, Movie

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'poster', 'year', 'country', 'directors', 'actors', 'genres', 'category']

    def create(self, validated_data):
        genres_data = validated_data.pop('genres', [])
        category_data = validated_data.pop('category', None)

        # Створення нового фільму без визначеного ID
        movie = Movie.objects.create(category=category_data, **validated_data)

        # Додавання жанрів до фільму
        if genres_data:
            movie.genres.set(genres_data)

        return movie

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres', None)
        category_data = validated_data.pop('category', None)

        # Оновлюємо категорію
        if category_data:
            instance.category = category_data

        # Оновлюємо атрибути фільму
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Збереження змін
        instance.save()

        # Оновлюємо жанри
        if genres_data is not None:
            instance.genres.set(genres_data)

        return instance
