from django.http import Http404
from django.shortcuts import render
from datetime import datetime
from .models import Series, Match, Message


def index(request):
	now = datetime.today()
	todays_matches = Match.objects.filter(date__day=now.day, date__month=now.month, date__year=now.year).order_by('date','time')
	upcoming_matches = Match.objects.filter(date__gt=now).order_by('date', 'time')[:20]
	recent_matches = Match.objects.filter(date__lt=now).order_by('-date', '-time')[:20]
	all_series = Series.objects.all().order_by('-date')[:5]


	recent_count = Match.objects.filter(date__lt=now).count()
	predicted = Match.objects.exclude(prediction='').count()	
	won = Match.objects.filter(result='pass').count()

	try:
	    accuracy = int((won/predicted)*100)
	except ZeroDivisionError:
	    accuracy = 0	

	context = {
		'todays_matches' : todays_matches,
		'upcoming_matches' : upcoming_matches,
		'recent_matches' : recent_matches,		
		'all_series' : all_series,

		#stats related
		'recent_count' : recent_count,
		'predicted' : predicted,
		'won' : won,
		'accuracy' : accuracy,
	}
	return render(request, 'match/index.html', context)


def match_detail(request, slug):
	try:
		match = Match.objects.get(slug=slug)
		series = Series.objects.get(pk=match.series.id)
		schedule = series.match_set.all().order_by('date')
		messages = match.message_set.all()
		return render(request, 'match/match_detail.html', context={'series':series, 'schedule':schedule, 'match':match, 'messages':messages})
	except Match.DoesNotExist:
		return render(request, 'match/404.html')


def upcoming_matches(request):
	now = datetime.today()
	upcoming_matches = Match.objects.filter(date__gt=now).order_by('date', 'time')

	return render(request, 'match/upcoming_matches.html', context={'upcoming_matches' : upcoming_matches})

