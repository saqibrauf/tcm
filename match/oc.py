import requests
import sched, time
from bs4 import BeautifulSoup
from match.models import Match

class OddsChecker():

	odds_url = ''
	bookie = ''

	def odds(self):
		odds_url = self.odds_url
		bookie = self.bookie
		odds_response = requests.get(odds_url)
		odds_html = odds_response.content
		odds_soup = BeautifulSoup(odds_html, 'html.parser')
		
		if bookie  == 'betfair': #BETFAIR ODDS NO IS 25
			b_no = 25
		elif bookie == 'betdaq': #BETDAQ ODDS NO IS 26
			b_no = 26
		elif bookie == 'bet365':
			b_no = 1
		
		try:
			TA = odds_soup.find_all('tr',class_='diff-row')[0]
			TA_NAME = TA['data-bname']
			TA_ODDS = TA.find_all('td')[b_no]
			TA_ODDS = TA_ODDS['data-odig']
			if not TA_ODDS:
				TA_ODDS = '0'

			TB = odds_soup.find_all('tr',class_='diff-row')[1]
			TB_NAME = TB['data-bname']
			TB_ODDS = TB.find_all('td')[b_no]
			TB_ODDS = TB_ODDS['data-odig']
			if not TB_ODDS:
				TB_ODDS = '0'

			odds_list = (TA_NAME, TA_ODDS, TB_NAME, TB_ODDS)
			
			return odds_list

		except:
			print('No Odds Found For ' + bookie)
			odds_list = ('0','0','0','0')
			return odds_list
			pass

class ScoreBoard():

	score_url = ''
	
	def score(self):
		score_url = self.score_url
		score_response = requests.get(score_url)
		score_html = score_response.content
		score_soup = BeautifulSoup(score_html, 'html.parser')

		#Main DIV
		score_data = score_soup.find(class_= 'cscore_competitors')

		#Foot Notes		
		try:
			foot_note = score_soup.find(class_='cscore_notes_game')
			comm = foot_note.get_text()
		except:
			comm = 'Not updated'
			print ('Commentry not found...')
			pass
		
		#Names
		try:
			teams = score_soup.find_all(class_='cscore_name--long')
			t1 = teams[0].get_text()
			t2 = teams[1].get_text()
		except:
			t1 = 'Not Updated'
			t2 = 'Not Updated'
			print ('Teams not found...')
			pass

		#Score
		try:
			runs = score_soup.find_all(class_='cscore_score')
			s1 = runs[0].get_text()
			s2 = runs[1].get_text()
		except:
			s1 = 'Not Updated'
			s2 = 'Not Updated'
			print ('Scores not found...')
			pass

		score_list = (t1, s1, t2, s2, comm)

		return score_list

def store_data():
	
	match = Match.objects.filter(status='live').exclude(score_url__isnull=True, odds_url__isnull=True).exclude(score_url__exact='', odds_url__exact='')

	if match:

		for m in match:

			score_url = m.score_url
			score = ScoreBoard()
			score.score_url = score_url
			data = score.score()

			bookie = m.bookie
			odds_url = m.odds_url
			odds = OddsChecker()
			odds.bookie = bookie
			odds.odds_url = odds_url
			odds_data = odds.odds()

			m.team_a = data[0]
			m.team_a_score = data[1]
			m.team_b = data[2]
			m.team_b_score = data[3]
			m.notes = data[4]

			m.odds_team_a_name = odds_data[0]
			m.team_a_odds = odds_data[1]
			m.odds_team_b_name = odds_data[2]
			m.team_b_odds = odds_data[3]
			
			m.save()

			print(data)
			print(odds_data)
			print ('Storing Data=============================================================================')

	else:

		print('No Live Match.....')


s = sched.scheduler(time.time, time.sleep)

def run_task(sc): 	
    store_data()
    s.enter(10, 1, run_task, (sc,))

s.enter(10, 1, run_task, (s,))

s.run()