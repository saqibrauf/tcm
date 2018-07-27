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
		try:
			foot_note = soup.find(class_='cscore_notes_game')
			comm = foot_note.get_text()
		except:
			comm = 'Not updated'
			print ('Commentry not found...')
			pass
		
		#Names
		try:
			teams = data.find_all(class_='cscore_name--long')
			t1 = teams[0].get_text()
			t2 = teams[1].get_text()
		except:
			t1 = 'Not Updated'
			t2 = 'Not Updated'
			print ('Teams not found...')
			pass

		#Score
		try:
			runs = data.find_all(class_='cscore_score')
			s1 = runs[0].get_text()
			s2 = runs[1].get_text()
		except:
			s1 = 'Not Updated'
			s2 = 'Not Updated'
			print ('Scores not found...')
			pass

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

		print ('Storing Data...')

	else:

		print('No Live Match.....')


s = sched.scheduler(time.time, time.sleep)

def run_task(sc): 	
    store_data()
    s.enter(10, 1, run_task, (sc,))

s.enter(10, 1, run_task, (s,))

s.run()

