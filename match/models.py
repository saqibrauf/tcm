from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone


#Main series table
class Series(models.Model):
	date = models.DateTimeField(default=timezone.now)
	title = models.CharField(max_length=255, default='Enter Series Title')
	series_slug = models.SlugField(max_length=255, default='', editable=False)
	summary = models.TextField(blank=True)
	series_image = models.FileField(default='game.png')

	def __str__(self):
		return self.title.upper()

	def save(self, *args, **kwargs):
		self.title = self.title.lower()
		self.series_slug = slugify(self.title)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('series_detail', args=[str(self.series_slug)])

	class Meta:
		verbose_name_plural = 'All Series'
		ordering = ['-date']


#Matches in Tournament
class Match(models.Model):
	series = models.ForeignKey(Series, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now, editable=False)
	opponents = models.CharField(max_length=255, default='Add Opponents')
	slug = models.SlugField(max_length=255, default='', editable=False)
	prediction = models.CharField(max_length=50, blank=True)
	winner = models.CharField(max_length=50, blank=True)
	PR_RESULT = (
		('pass', 'Pass'),
		('fail', 'Fail'),
		('no result', 'No Result'),
	)
	result = models.CharField(max_length=10, choices=PR_RESULT, default='no result')

	def __str__(self):
		return self.opponents.upper()

	def save(self, *args, **kwargs):
		self.opponents = self.opponents.lower()
		self.prediction = self.prediction.lower()
		self.winner = self.winner.lower()
		self.slug = slugify(self.opponents) + '-' + self.series.series_slug
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('match_detail', args=[str(self.slug)])

	class Meta:
		verbose_name_plural='All Matches'
		ordering = ['-date']

#Messages in Match

class Message(models.Model):
	match = models.ForeignKey(Match, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now, editable=False)
	message = models.TextField(max_length=255)

	def __str__(self):
		return self.match.opponents.upper()

	class Meta:
		verbose_name_plural = 'All Messages'
		ordering = ['-date']