from django.core.management.base import BaseCommand

from movies.jobs import CinemaLaPlataImporter, VillageCinesImporter

__author__ = 'saczuac'


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Start the scrapping process."""
        cinemalaplata_site = 'http://www.cinemalaplata.com/'
        villagecines_site = 'https://www.villagecines.com'

        CinemaLaPlataImporter(
            site=cinemalaplata_site,
        ).import_all_movies()

        print "Scrapping of " + cinemalaplata_site + "had been done succesfully!"

        VillageCinesImporter(
            site=villagecines_site,
        ).import_all_movies()

        print "Scrapping of " + villagecines_site + "had been done succesfully!"
