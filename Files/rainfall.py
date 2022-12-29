import settings

from gpiozero import Button
rain_sensor = Button(6, pull_up=True)
settings.rain_count = 0	
settings.rain_count_daily = 0	

def bucket_tipped():
	settings.rain_count = settings.rain_count + 1
	settings.rain_count_daily = settings.rain_count_daily + 1
	
	print(settings.rain_count * settings.BUCKET_SIZE)
	print(settings.rain_count_daily * settings.BUCKET_SIZE)
	
rain_sensor.when_pressed = bucket_tipped
