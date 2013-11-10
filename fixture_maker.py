import json
import pickle
import os

events = pickle.load(open('events.pkl'))
events_wrapped = []
for event in events:
	events_wrapped.append({"model":"website.Event","fields":event})

with open(os.path.join("foodfinder","website","fixtures","fixtures.json"),'w') as output:
	output.write(json.dumps(events_wrapped))