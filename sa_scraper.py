import json
import re
import urllib2

class sa_scraper:
	def scrape(self):
		sa_data = urllib2.urlopen("https://www.googleapis.com/calendar/v3/calendars/utulsa.edu_phngeno8i8nb54u70nepv793m0%40group.calendar.google.com/events?orderBy=startTime&singleEvents=true&timeZone=America%2FChicago&key=AIzaSyBYMs84E3yw0NhKiC8i24Xifukh8du8RrM")
		sa_data = sa_data.read()
		sa_data = json.loads(sa_data)
		print sa_data

scrape = sa_scraper()
scrape.scrape()