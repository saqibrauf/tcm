from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from .models import Series, Match, Message


def index(request):
	now = timezone.now()

	today_matches = Match.objects.filter(date__day=now.day, date__month=now.month, date__year=now.year).order_by('date')	
	
	upcoming_matches = Match.objects.filter(date__gt=now).exclude(date__day=now.day, date__month=now.month, date__year=now.year).order_by('date')

	recent_matches = Match.objects.filter(date__lt=now).exclude(date__day=now.day, date__month=now.month, date__year=now.year).order_by('-date')

	all_series = Series.objects.order_by('-date')

	latest_series = Series.objects.order_by('-date')

	latest_match = Match.objects.filter(date__gt=now).order_by('date')

	context = {
		'today_matches' : today_matches,
		'upcoming_matches' : upcoming_matches,
		'recent_matches' : recent_matches,		
		'all_series' : all_series,
		'latest_series' : latest_series,
		'latest_match' : latest_match,
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
	now = timezone.now()
	upcoming_matches = Match.objects.filter(date__gt=now).order_by('date')

	return render(request, 'match/upcoming_matches.html', context={'upcoming_matches' : upcoming_matches})


def series_detail(request, slug):
	series = Series.objects.get(series_slug=slug)
	schedule = series.match_set.all().order_by('date')

	return render(request, 'match/series_detail.html', context={'series' : series, 'schedule' : schedule})



#ScoreCard AJAX
from django.http import JsonResponse
def scorecard(reuest):

	pk = reuest.GET.get('pk', None)
	match = Match.objects.get(pk=pk)
	data = [match.team_a, match.team_a_score, match.team_b, match.team_b_score, match.notes, match.prediction]

	return JsonResponse(data, safe=False)
