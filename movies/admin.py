# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from movies.models import Language, Movie, Cinema, Genre
from movies.models import Function, Room

admin.site.register(Language)
admin.site.register(Cinema)
admin.site.register(Movie)
admin.site.register(Function)
admin.site.register(Genre)
admin.site.register(Room)
