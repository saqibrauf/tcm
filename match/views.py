from django.http import Http404
from django.shortcuts import render
from datetime import datetime
from .models import Series, Match, Message


def index(request):
	now = datetime.today()
	todays_matches = Match.objects.filter(date__day=now.day, date__month=now.month, date__year=now.year).order_by('date','time')
	upcoming_matches = Match.objects.filter(date__gt=now).order_by('date')
	recent_matches = Match.objects.filter(date__lt=now).order_by('-date')
	all_series = Series.objects.all().order_by('-date')[:5]
	return render(request, 'match/index.html', context={'todays_matches':todays_matches, 'upcoming_matches':upcoming_matches, 'recent_matches':recent_matches, 'all_series':all_series})


def match_detail(request, slug):
	try:
		match = Match.objects.get(slug=slug)
		series = Series.objects.get(pk=match.series.id)
		schedule = series.match_set.all().order_by('date')
		messages = match.message_set.all()
		return render(request, 'match/detail.html', context={'series':series, 'schedule':schedule, 'match':match, 'messages':messages})
	except Match.DoesNotExist:
		return render(request, 'match/404.html')
