from datetime import datetime, timedelta, time, date
import settings
import logging

#logging.basicConfig(level=logging.INFO, filename='/home/pi/weather-station/app.log', filemode='a',format='%(asctime)s %(message)s')

def reset_rainfall():

	now = datetime.now()
	settings.hourInTheDay = now.hour
	#print('Hour in the day is: ',settings.hourInTheDay)

	today = date.today() 
	settings.dateInTheMonth = today.day ## i.e if date is 8-March, today = 8
	#print('Date in the month is: ',settings.dateInTheMonth)

	if settings.savedHourInTheDay != settings.hourInTheDay:
		print('reset hourly rainfall')
		logging.info('reset hourly rainfall')
		settings.savedHourInTheDay = settings.hourInTheDay
		settings.rain_count = 0

	if settings.savedDayOfTheWeek != settings.dateInTheMonth:
		print('reset daily rainfall')
		logging.info('reset daily rainfall')
		settings.savedDayOfTheWeek = settings.dateInTheMonth            
		settings.rain_count_daily = 0
		
	#print(settings.savedHourInTheDay, settings.hourInTheDay, settings.savedDayOfTheWeek, settings.dateInTheMonth)
			



