from django.db import models
from datetime import datetime
from django.template.defaultfilters import slugify
from django.urls import reverse


#Main series table
class Series(models.Model):
	date = models.DateField(default=datetime.today)
	title = models.CharField(max_length=255, default='Enter Tournament Title')
	series_slug = models.SlugField(max_length=255, default='', editable=False)
	summary = models.TextField(default='Summary', blank=True)
	series_image = models.FileField(default='game.png')

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.series_slug = slugify(self.title)
		super().save(*args, **kwargs)

	class Meta:
		verbose_name_plural = 'Series'
		ordering = ['-date']

    	
#Matches in Tournament
class Match(models.Model):	
	series = models.ForeignKey(Series, on_delete=models.CASCADE)
	date = models.DateField(default=datetime.now)
	time = models.TimeField(default=datetime.now)
	opponents = models.CharField(max_length=255, default='Opponents')
	slug = models.SlugField(max_length=255, default='', editable=False)
	ST_CHOICE = (
		('Live', 'Live'),
		('Upcoming', 'Upcoming'), 
		('Recent', 'Recent'),
	)
	status = models.CharField(max_length=8, choices=ST_CHOICE, default='Upcoming')
	prediction = models.CharField(max_length=50, default='Not Updated')
	winner = models.CharField(max_length=50, default='Not Updated')
	PR_RESULT = (
		('Pass', 'Pass'),
		('Fail', 'Fail'),
		('No Result', 'No Result'),
	)
	result = models.CharField(max_length=10, choices=PR_RESULT, default='No Result')

	def __str__(self):
		return self.opponents

	def save(self, *args, **kwargs):
		self.slug = slugify(self.opponents)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('match_detail', args=[str(self.slug)])
	
	class Meta:
		verbose_name_plural='Matches'
		ordering = ['-date']

#Messages in Match

class Message(models.Model):
	match = models.ForeignKey(Match, on_delete=models.CASCADE)
	date = models.DateTimeField(default=datetime.now)
	message = models.TextField(max_length=255, default='Admin message')

	def __str__(self):
		return self.match.opponents

	class Meta:
		ordering = ['-date']