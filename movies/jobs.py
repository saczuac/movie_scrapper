import os
import requests

from movies.models import Language, Movie, Cinema, Genre
from movies.models import Function, Room

from bs4 import BeautifulSoup

__author__ = "ferminmine"
__credits__ = ["saczuac", ]


class Importer:

    # Get a BeautifulSoup object ready to scrap
    def get_data(self, url):
        main_page = requests.get(url)
        data = main_page.text
        return BeautifulSoup(data, 'html.parser')


class CinemaLaPlataImporter(Importer):

    site = 'http://www.cinemalaplata.com/'
    output_file = False

    def import_all_movies(self):
        details = self.get_detail_pages()
        for detail_url in details:
            self.import_movie(detail_url)
        print "Scrapping of http://www.cinemalaplata.com/ had been done succesfully!"

    #  Given an URL of a movie, imports the data
    def import_movie(self, detail_url):
        scrap_detail = self.get_data(detail_url)
        movie = Movie()
        movie.title = scrap_detail.find("div", class_="page-title").text.strip().lower().encode('utf-8')
        movie.genre = scrap_detail.find(id="ctl00_cph_lblGenero").text.strip().lower().encode('utf-8')

        cinemas = scrap_detail.find(id="ctl00_cph_pnFunciones").find_all(class_='col-2')

        for cinema in cinemas:
            cinema_movie = movie
            cinema_data = cinema.find("span").text.split('-')
            cinema_movie.cinema = cinema_data[0].strip().lower().encode('utf-8')
            cinema_movie.room = cinema_data[1].strip().lower().encode('utf-8')
            functions = cinema.find('p').find_all('span')
            for function in functions:
                function_movie = cinema_movie
                function_data = function.text.split(':', 1)
                function_movie.language = function_data[0].strip().lower().encode('utf-8')
                hours = function_data[1].split('-')
                for hour in hours:
                    function_hour = function_movie
                    function_hour.hour = hour.strip().lower().encode('utf-8')
                    self.persist_movie(function_hour)

    def persist_movie(self, movie):
        filename = "../data/cinema_la_plata.txt"
        if self.output_file:
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
            self.output_file = True

        file = open(filename, append_write)
        file.write(movie.as_text_entry() + '\n')
        file.close()

    # Get all detail pages of movies from CinemaLaPlata
    def get_detail_pages(self):
        soup = self.get_data(self.site + 'cartelera.aspx')

        details = list()
        for link in soup.select('[href*=sinopsis]'):
            details.append(self.site + link.get('href'))

        return set(details)

