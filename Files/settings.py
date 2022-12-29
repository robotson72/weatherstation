def init():
	global ambient_temperature
	global pressure
	global humidity 
	global rain_count
	global rain_count_daily
	global rainfall # accumulated rainfall in the past 60 mins
	global wind_gust
	global wind_speed
	global wind_dir_average
	global rainfalldaily # rain so far today
	global goodmeasure
	global badmeasure
	global savedHourInTheDay
	global savedDayOfTheWeek
	global hourInTheDay
	global dateInTheMonth
	global ds18b20_probe

BUCKET_SIZE = 0.2794 # 0.2794 mm of rain will tip the bucket (1 reed switch pulse)

