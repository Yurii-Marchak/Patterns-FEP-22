from django.urls import path
from . import views
from .views import movies, PublicMovieView, AdminMovieView

urlpatterns = [
    path('', views.movies, name='movies'),
    path('api/movies/', PublicMovieView.as_view(), name='public-api-movies'),
    path('api/admin/movies/', AdminMovieView.as_view(), name='admin-api-movies'),
    path('api/admin/movies/<int:pk>/', AdminMovieView.as_view(), name='admin-api-movie-detail'),
    path('add_movie/', views.add_movie, name='add_movie'),
]

