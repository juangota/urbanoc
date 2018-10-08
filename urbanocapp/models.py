# coding=utf8
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

from lib.common_models import ModelsCommons


class Author(ModelsCommons):
	'''
	Authors model.

	Stores information about the author of an Urban Ocurrence
	'''
	name = models.CharField(unique=True, max_length=500)
	email = models.CharField(max_length=200, blank=True)
	phone = models.CharField(max_length=25, blank=True)

	def __str__(self):
		'''
		A string representation of the model.
		'''
		return self.name

	class Meta:
		app_label = "urbanocapp"


class OcurrenceLocation(ModelsCommons):
	'''
	Locations of ocurrences model.

	Stores the information about Urban Icurrences locations
	'''
	name = models.CharField(unique=True, max_length=200)
	longitude = models.FloatField()
	latitude = models.FloatField()

	point = models.PointField()
	objects = models.GeoManager()

	def save(self, *args, **kwargs):
		self.point = Point(self.longitude, self.latitude)
		super(OcurrenceLocation, self).save(*args, **kwargs) # Call the "real" save() method.

	def __str__(self):
		'''
		A string representation of the model.
		'''
		return self.name

	class Meta:
		unique_together = ('name', 'longitude','latitude',)
		app_label = "urbanocapp"
	

class UrbanOcurrence(ModelsCommons):
	'''
	Urban ocurrence model.

	Stores the Urban Ocurrences informations
	'''
	OCURRENCE_STATUS = [('not_validated','Not validated'),
						('validated','Validated'),
						('solved','Solved')]

	OCURRENCE_CATEGORY = [('construction','Planned road work'),
						  ('special_event','Special events \
										    (fair, sport event, etc.)'),
						  ('incident','Accidents and other unexpected events'),
						  ('weather_condition','Weather condition \
											    affecting the road'),
						  ('road_condition','Status of the road that \
						  					 might affect travellers \
						  					 (potholes, bad pavement, etc.)')]

	creator = models.ForeignKey(User, related_name="ocurrence_creator")
	author = models.ForeignKey(Author, related_name="ocurrence_author")
	description = models.TextField(default="", blank=True)
	location = models.ForeignKey(OcurrenceLocation, 
								 related_name="ocurrence_location")
	status = models.CharField(choices=OCURRENCE_STATUS,
							  default="not_validated", max_length=13)
	category = models.CharField(choices=[x for x in OCURRENCE_CATEGORY],
								default="", max_length=100)

	class Meta:
		app_label = "urbanocapp"