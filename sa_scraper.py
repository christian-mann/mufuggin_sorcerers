import json
import re
import urllib2
import pickle

class sa_scraper:
	def scrape(self):
		sa_data = urllib2.urlopen("https://www.googleapis.com/calendar/v3/calendars/utulsa.edu_phngeno8i8nb54u70nepv793m0%40group.calendar.google.com/events?orderBy=startTime&singleEvents=true&timeZone=America%2FChicago&key=AIzaSyBYMs84E3yw0NhKiC8i24Xifukh8du8RrM")
		sa_data = sa_data.read()
		sa_data = json.loads(sa_data)
		events = sa_data['items']
		events_simple = []
		for event in events:
			#Names used by model
			new_event = {'title':'','start_time':'','end_time':'','notes':''}
			if 'summary' in event.keys():
				new_event['title'] = event['summary'].encode('utf-8')
			if 'start' in event.keys():		
				if 'date' in event['start'].keys():
					new_event['start_time'] = event['start']['date'].encode('utf-8')
				if 'dateTime' in event['start'].keys():
					new_event['start_time'] = event['start']['dateTime'].encode('utf-8')
			if 'end' in event.keys():			
				if 'date' in event['end'].keys():
					new_event['end_time'] = event['end']['date'].encode('utf-8')
				if 'dateTime' in event['end'].keys():
					new_event['end_time']  = event['end']['dateTime'].encode('utf-8')
			if 'description' in event.keys():
				new_event['notes'] = event['description'].encode('utf-8')
			if 'location' in event.keys():
				new_event['location'] = event['location'].encode('utf-8')
			
			events_simple.append(new_event)
		#end loop	
		hits = ('free','food','lunch')
		for event in events_simple:
			event['food'] = any(hit in event['notes'] for hit in hits)
				
		with  open('events.pkl','w') as output:
			pickle.dump(events_simple, output)

scrape = sa_scraper()
scrape.scrape()