from django.core.management.base import BaseCommand

from movies.jobs import CinemaLaPlataImporter

__author__ = 'saczuac'


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Start the scrapping process."""
        site = 'http://www.cinemalaplata.com/'
        output_file = False

        CinemaLaPlataImporter(
            site=site,
            output_file=output_file
        ).import_all_movies()

        print "Scrapping of " + site + "had been done succesfully!"
