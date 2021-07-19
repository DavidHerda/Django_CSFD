from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from browser.models import Actor, Movie
from django.core.paginator import Paginator
from django.db.models import Q

def search(request):
    
    if request.method == "POST":

        user_input = request.POST['input']

        found_movies = Movie.objects.filter(Q(title_unidecode__contains=user_input) | Q(title__contains=user_input))
        found_actors = Actor.objects.filter(Q(name_unidecode__contains=user_input) | Q(name__contains=user_input))
        
        context = {'input': user_input, 'movies': found_movies, 'actors': found_actors}

        return render(request, 'search.html', context)

    else:
        return render(request, 'search.html')


def actor_details(request, id):

    actor = get_object_or_404(Actor, pk=id)
    actor_movies = actor.movies.all()
    
    context = {'actor': actor, 'actor_movies': actor_movies}

    return render(request, 'actor_details.html', context)

def movie_details(request, id):

    movie = get_object_or_404(Movie, pk=id)
    movie_cast = movie.actors.all()

    context = {'movie': movie, 'movie_cast': movie_cast}

    return render(request, 'movie_details.html', context)


def movies_list(request):

    p = Paginator(Movie.objects.all(), 20)
    page = request.GET.get('page')
    movies = p.get_page(page)

    context = {'movies': movies}

    return render(request, 'movies_list.html', context)

def actors_list(request):

    p = Paginator(Actor.objects.all(), 100)
    page = request.GET.get('page')
    actors = p.get_page(page)

    context = {'actors': actors}

    return render(request, 'actors_list.html', context)
