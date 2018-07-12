import requests
import sched, time
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
		foot_note = soup.find(class_='cscore_notes_game')

		if foot_note:
			comm = foot_note.get_text()
		else:
			comm = 'Not Updated'
		

		#CHILD DIVS
		if data.find_all(class_='cscore_name--long'):
			teams = data.find_all(class_='cscore_name--long')
		if data.find_all(class_='cscore_score'):
			runs = data.find_all(class_='cscore_score')

		if teams:
			t1 = teams[0].get_text()
			t2 = teams[1].get_text()
		else:
			t1 = 'Not Updated'
			t2 = 'Not Updated'

		if runs:
			s1 = runs[0].get_text()
			s2 = runs[1].get_text()
		else:
			s1 = 'Not Updated'
			s2 = 'Not Updated'

		list = (t1, s1, t2, s2, comm)

		return list

def store_data():
	
	match = Match.objects.filter(status='live').exclude(score_url__isnull=True).exclude(score_url__exact='')

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


s = sched.scheduler(time.time, time.sleep)

def run_task(sc): 
    print ("Doing stuff...")
    store_data()
    s.enter(10, 1, run_task, (sc,))

s.enter(10, 1, run_task, (s,))

s.run()

