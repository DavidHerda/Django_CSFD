from django.urls import path
from . import views

urlpatterns = [
path("", views.search, name="search"),
path("actors/", views.actors_list, name="actors"),
path("actors/<int:id>", views.actor_details, name="actor"),
path("movies/", views.movies_list, name="movies"),
path("movies/<int:id>", views.movie_details, name="movie")
]