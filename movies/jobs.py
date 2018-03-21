# -*- coding: utf-8 -*-
import requests

from movies.models import Language, Movie, Cinema, Genre
from movies.models import Function, Room

from django.db.utils import IntegrityError

from bs4 import BeautifulSoup

__author__ = "ferminmine"
__credits__ = ["saczuac", ]


class CinemaImporter:

    def __init__(self, *args, **kwargs):
        self.site = kwargs['site']

    # Get a BeautifulSoup object ready to scrap
    def get_data(self, url):
        main_page = requests.get(url)
        data = main_page.text
        return BeautifulSoup(data, 'html.parser')

    def import_all_movies(self):
        pass

    def persist_genre(self, name):
        genre, created = Genre.objects.get_or_create(name=name)
        return genre

    def persist_movie(self, title, genre, distributor=None):
        try:
            movie, created = Movie.objects.get_or_create(
                title=title, genre=genre, distributor=None)
        except IntegrityError:
            # Movie exists
            return Movie.objects.get(title=title)
        return movie

    def persist_room(self, name, cinema):
        room, created = Room.objects.get_or_create(name=name, cinema=cinema)
        return room

    def persist_cinema(self, name):
        cinema, created = Cinema.objects.get_or_create(name=name)
        return cinema

    def persist_language(self, name):
        language, created = Language.objects.get_or_create(name=name)
        return language

    def persist_function(self, movie, room, language, hour):
        function, created = Function.objects.get_or_create(
            movie=movie,
            room=room,
            language=language,
            from_hour=hour
        )

        return function


class CinemaLaPlataImporter(CinemaImporter):

    def import_all_movies(self):
        details = self.get_detail_pages()

        for detail_url in details:
            self.import_movie(detail_url)

    def import_movie(self, detail_url):
        #  Given an URL of a movie, imports the data
        scrap_detail = self.get_data(detail_url)

        title = scrap_detail.find(
            "div", class_="page-title"
        ).text.strip().lower().encode('utf-8')

        genre_name = scrap_detail.find(
            id="ctl00_cph_lblGenero"
        ).text.strip().lower().encode('utf-8')

        genre = self.persist_genre(genre_name)
        movie = self.persist_movie(title, genre)

        cinemas = scrap_detail.find(id="ctl00_cph_pnFunciones").find_all(class_='col-2')

        for cinema in cinemas:
            data = cinema.find("span").text.split('-')
            cinema_name = data[0].strip().lower().encode('utf-8')
            room_name = data[1].strip().lower().encode('utf-8')

            cine = self.persist_cinema(cinema_name)
            room = self.persist_room(room_name, cine)

            functions = cinema.find('p').find_all('span')

            for function in functions:
                function_data = function.text.split(':', 1)

                language_name = function_data[0].strip().lower().encode('utf-8')
                language = self.persist_language(language_name)
                hours = function_data[1].split('-')

                for hour in hours:
                    hour = hour.strip().lower().encode('utf-8')
                    self.persist_function(movie, room, language, hour)

    # Get all detail pages of movies from CinemaLaPlata
    def get_detail_pages(self):
        soup = self.get_data(self.site + 'cartelera.aspx')
        details = list()

        for link in soup.select('[href*=sinopsis]'):
            details.append(self.site + link.get('href'))

        return set(details)  # Remove duplicateds


class VillageCinesImporter(CinemaImporter):

    def import_all_movies(self):
        details = self.get_detail_pages()

        for detail_url in details:
            self.import_movie(detail_url)

    def import_movie(self, detail_url):
        #  Given an URL of a movie, imports the data
        scrap_detail = self.get_data(detail_url)

        title = scrap_detail.find(
            "title").text.split("-")[0].strip().lower().encode('utf-8')

        info = scrap_detail.find(
            id="ficha-tecnica"
        )

        if not info:
            info = scrap_detail.find(
                class_="col-lg-5 col-md-5"
            )

        genre_name = info.text.split("<strong>")[0].split(
            u"Género:")[1].split("\n")[0].strip().lower().encode('utf-8')

        distributor = None

        try:
            distributor = info.text.split("<strong>")[0].split(
                u"Distribuidora:")[1].split("\n")[0].strip().lower().encode('utf-8')
        except IndexError:
            #  Movie has not distributor
            pass

        genre = self.persist_genre(genre_name)
        self.persist_movie(title, genre, distributor)

    # Get all detail pages of movies from CinemaLaPlata
    def get_detail_pages(self):
        soup = self.get_data(self.site)
        details = list()

        for link in soup.select('[href*=peliculas/]'):
            details.append(link.get('href'))

        return set(details)  # Remove duplicateds
