from django.core.management.base import BaseCommand, CommandError
from browser.models import Movie,Actor
from browser.csfd_scrape import scrape_movies, scrape_movie_cast
import time
import unidecode

class Command(BaseCommand):
    help = 'Scrape CSFD and populate database'

    def add_arguments(self, parser):
        parser.add_argument('runscrape', action='store_true')


    def handle(self, *args, **options):

        if Movie.objects.all().count() == 0:

            scraped_movies_info = scrape_movies()

            for movie_info in scraped_movies_info:            
                movie_title = movie_info[0].text.strip()
                movie_year = movie_info[1]
                print(movie_title, movie_year)
                movie = Movie.objects.create(title=movie_title, title_unidecode=unidecode.unidecode(movie_title), year=movie_year)
                scraped_actors = scrape_movie_cast(movie_info[0]['href'])

                for scraped_actor in scraped_actors:
                    actor, created = Actor.objects.get_or_create(name=scraped_actor, name_unidecode=unidecode.unidecode(scraped_actor))
                    actor.movies.add(movie)                 
                    movie.actors.add(actor)

                time.sleep(0.5)

            print("CSFD scrape done")
        else:
            print("DB already populated with scraped data")