import requests
from bs4 import BeautifulSoup
from match.models import Match

class ScoreBoard():

	url = ''
	
	def score(self):

		url = self.url

		response = requests.get(url)
		html = response.content

		soup = BeautifulSoup(html, 'html.parser')

		#Main DIV
		data = soup.find(class_= 'cscore_competitors')

		#Foot Notes
		comm = soup.find_all(class_='cscore_notes_game')
		comm = comm[0].get_text()

		#CHILD DIVS
		teams = data.find_all(class_='cscore_name--long')
		runs = data.find_all(class_='cscore_score')

		t1 = teams[0].get_text()
		t2 = teams[1].get_text()
		s1 = runs[0].get_text()
		s2 = runs[1].get_text()

		list = (t1, s1, t2, s2, comm)

		return list

def store_data():
	
	match = Match.objects.filter(status='live').exclude(score_url__isnull=True).exclude(score_url__exact='')

	qty = match.count()

	if match:

		for m in match:

			url = m.score_url

			score = ScoreBoard()

			score.url = url

			data = score.score()

			m.team_a = data[0]
			m.team_a_score = data[1]
			m.team_b = data[2]
			m.team_b_score = data[3]
			m.notes = data[4]
			m.save()