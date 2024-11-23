from django.db import models
from django.urls import reverse

class Category(models.Model):
    """Категорії"""
    name = models.CharField("Категорія", max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Genre(models.Model):
    """Жанри"""
    name = models.CharField("Ім'я", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"


class Movie(models.Model):
    """Фільм"""
    title = models.CharField("Назва", max_length=100)
    description = models.TextField("Опис", default="")  
    poster = models.CharField("Постер", max_length=200, default="")
    year = models.PositiveSmallIntegerField("Дата виходу", default=0)
    country = models.CharField("Країна", max_length=30, default="")  
    directors = models.TextField("Режисер", default="") 
    actors = models.TextField("Актори", null=True, blank=True, default="")  
    genres = models.ManyToManyField(Genre, verbose_name="Жанри")
    category = models.ForeignKey(
        Category, verbose_name="Категорія", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фільм"
        verbose_name_plural = "Фільми"
