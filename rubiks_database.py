import pyrebase
from datetime import datetime

# Configure Firebase
config = {
  "apiKey": "AIzaSyDyTulUCX5swJauYm8YM55Vr5a5vv8ipPQ",
  "authDomain": "rubiksscanner.firebaseapp.com",
  "databaseURL": "https://rubiksscanner.firebaseio.com",
  "storageBucket": "rubiksscanner.appspot.com"
}

# Get database
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Add info to database given id of competitor and array of 5 strings representing
# the times it took to complete each round
def addInfoToDatabase(id, times): 
	all_times = []
	for r, time in enumerate(times):
		# add each round's time to database
		round = r + 1
		db.child("EventName").child("Competitors").child(id).child(round).set(time)

		# get time in total seconds
		divided = time.split(":")
		minutes = divided[0]
		seconds = divided[1]
		miliseconds = divided[2]
		total_seconds = float(minutes)*60 + float(seconds) + float(miliseconds)*0.001
		#print(total_seconds)
		
		# add each time to list
		all_times.append(total_seconds)

	# remove max and min time from list
	all_times.remove(max(all_times))
	all_times.remove(min(all_times))

	# compute average of remaining times
	average_time = sum(all_times)/3
	#print(average_time)

	# convert average time back to string format
	int_time = int(average_time)

	miliseconds = "%.3f" % (average_time - int_time)
	minutes = int(average_time / 60)
	seconds = int_time - minutes*60

	# add 0 to front of minutes if <10
	minutes = str(minutes)
	if len(minutes) == 1:
		minutes = "0" + minutes

	# same with seconds
	seconds = str(seconds)
	if len(seconds) == 1:
		seconds = "0" + seconds


	avg_string = minutes + ":" + seconds + "." + str(miliseconds[2:])
	#print(avg_string)

	# add the new string and average seconds to database
	db.child("EventName").child("Competitors").child(id).child("seconds").set(average_time)
	db.child("EventName").child("Competitors").child(id).child("avg").set(avg_string)

# Return Dictionary of competitors organized in order of average completion time
def getWinners():
	# dictionary of competitors
	winners_dict = {}
	competitors = db.child("EventName").child("Competitors").get()
    
    # add competitor id/times to dictionary
	for c in competitors.each():
		if type(c.val()) is dict:
			id = str(c.key())
			seconds = c.val()['seconds']
			#print(c.val()['seconds'])
			#print(c.key())
			winners_dict[id] = seconds
    
    # sort dictionary by average seconds
	ordered_winners = sorted(winners_dict.items(), key=lambda x: x[1])

	print("Winners") # Print winners
    
	place = 1
	for key, value in ordered_winners:
		# get average time for each competitor from database
		time = db.child("EventName").child("Competitors").child(str(key)).child('avg').get()
		print (str(place) + ". Competitor id " + str(key) + ": " + time.val())
		place += 1

	return ordered_winners

times = ["01:02:000", "01:06:000", "01:03:000", "01:55:000", "01:02:000"]
addInfoToDatabase("734", times)
getWinners()