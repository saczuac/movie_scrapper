# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _


class Language(models.Model):
	name = models.CharField(_('Lenguaje'), max_length=100, unique=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.name

    def __unicode__(self):
    	return u'%s' % self.name


class Room(models.Model):
	name = models.CharField(_('Nombre de Sala'), max_length=100, unique=True)

	cinema = models.ForeignKey(
		Cinema,
		verbose_name=_('Cine'),
		related_name='rooms'
	)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return self.name + ' from: ' + self.cinema.name

    def __unicode__(self):
    	return u'%s%s%s' % (self.name, ' from: ', self.cinema.name)


class Cinema(models.Model):
	name = models.CharField(_('Cinema'), max_length=150, unique=True)

    class Meta:
        verbose_name = "Cinema"
        verbose_name_plural = "Cinemas"

    def __str__(self):
        return self.name

    def __unicode__(self):
    	return u'%s' % self.name
    

class Genre(models.Model):
	name = models.CharField(_('Género'), max_length=100, unique=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

    def __unicode__(self):
    	return u'%s' % self.name


class Movie(models.Model):
	title = models.CharField(_('Título'), max_length=200, unique=True)

	genre = models.ForeignKey(
		Genre,
		verbose_name=_('Género'),
		related_name='movies'
	)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title + ' ' + self.genre.name


    def __unicode__(self):
    	return u'%s%s%s' % (self.title, ' ', self.genre.name)


class Function(models.Model):
	from_hour = models.DateTimeField()
	to_hour = models.DateTimeField()

	movie = models.ForeignKey(
		Movie,
		verbose_name=_('Película'),
		related_name='functions'
	)

	room = models.ForeignKey(
		Room,
		verbose_name=_('Sala'),
		related_name='functions'
	)

	language = models.ForeignKey(Language, verbose_name=_('Lenguaje'))

    class Meta:
        verbose_name = "Function"
        verbose_name_plural = "Functions"

    def __str__(self):
        return self.movie.name + ' => From: ' + str(self.from_hour) + ' To: ' str(self.to_hour) \
        		+ ' In: ' + self.room.name + ' Spoken in: ' + self.language.name \
        		+ ' From cinema: ' + self.room.cinema.name

    def __unicode__(self):
    	function_string = self.movie.name + ' => From: ' + str(self.from_hour) + ' To: ' str(self.to_hour) \
        		+ ' In: ' + self.room.name + ' Spoken in: ' + self.language.name \
        		+ ' From cinema: ' + self.room.cinema.name

    	return u'%s' % function_string
