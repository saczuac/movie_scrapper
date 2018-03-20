from django.core.management.base import BaseCommand

from movies.jobs import CinemaLaPlataImporter

__author__ = 'saczuac'


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Start the scrapping process."""
        CinemaLaPlataImporter().import_all_movies()
