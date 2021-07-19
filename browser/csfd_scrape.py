import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re

base_url = "https://www.csfd.cz/"
movies_url = "https://www.csfd.cz/zebricky/filmy/nejlepsi/?showMore=1"
user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def scrape_movies():
    
    r = session.get(movies_url, headers=user_agent)
    soup = BS(r.text, "html.parser")

    movie_titles = soup.find_all("a", href=True,class_="film-title-name")

    movie_years = soup.find_all(class_="film-title-info")
    movie_years = [int(re.sub('[()]','',y.text)) for y in movie_years]

    movies_info = zip(movie_titles, movie_years)

    return movies_info


def scrape_movie_cast(relative_url):

    url = urljoin(base_url, relative_url)    
    movie_details = session.get(url, headers=user_agent)
    soup = BS(movie_details.text, "html.parser")
    
    movie = soup.find(text="Hrají: ").parent
    target = movie.find_next_sibling('span').find_all('a')
    
    for _ in target:
        if _.text == "více" or _.text == "méně":
            target.remove(_)

    return [cast.text.strip() for cast in target]


