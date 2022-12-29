from datetime import datetime, timedelta, time
import timesched
import logging
import settings
import os
from threading import Thread
import threading
import time

import math
import bme280_sensor
import wind_direction_byo
import rainfall
import resetRainfall
import settings
import log_all_sensors_byo
import ds18b20_therm

from gpiozero import Button
import statistics

global wind_count

CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 60*60
ADJUSTMENT = 1.18
wind_speed_sensor = Button(5, pull_up=True)
wind_count = 0

radius_cm = 9.0
wind_interval = 5 # seconds
interval = 300 # seconds

store_speeds = []
store_directions = []

settings.init()				# call only once

path = "/home/pi/weather-station/app.log"

try: 
    os.remove(path) 
    print("% s removed successfully" % path) 
except OSError as error: 
    print(error) 
    print("File path can not be removed") 

logging.basicConfig(level=logging.INFO, filename='/home/pi/weather-station/app.log', filemode='a',format='%(asctime)s %(message)s')
logging.info('Logging started - V6 29/12/2022')

settings.rainfalldaily = 0
settings.rainfall = 0
settings.rain_count = 0
settings.rain_count_daily = 0
settings.savedDayOfTheWeek=0
settings.savedHourInTheDay=0
settings.hourInTheDay=0
settings.dateInTheMonth=0
                 
def reset_wind():
    global wind_count
    wind_count = 0

def spin(): # get 2 inputs per full rev
        global wind_count
        wind_count = wind_count + 1
        #print("spin " + str(wind_count))

def calculate_speed(time_sec):
        global wind_count
        circumference_cm = (2 * math.pi) * radius_cm
        rotations = wind_count / 2.0
        dist_km = (circumference_cm * rotations) / CM_IN_A_KM

        km_per_sec = dist_km / time_sec
        km_per_hour = km_per_sec * SECS_IN_AN_HOUR
        
        #print("calc speed ", wind_count, time_sec, km_per_hour * ADJUSTMENT)
        return km_per_hour * ADJUSTMENT

wind_speed_sensor.when_pressed = spin
temp_probe = ds18b20_therm.DS18B20()

while False:
    pass

while True:
        resetRainfall.reset_rainfall()
        
        start_time = time.time()
        while time.time() - start_time <= interval: # 300 seconds
            wind_start_time = time.time()
            reset_wind()
            #time.sleep(wind_interval) # during this time wait here and collect data
            while time.time() - wind_start_time <= wind_interval:  # 5 seconds
                store_directions.append(wind_direction_byo.get_value(wind_interval)) # gather direction data during 5 seconds

            # calc final_speed and update list every 5s
            final_speed = calculate_speed(wind_interval) # use no. of counts divided by time
            store_speeds.append(final_speed)

        # every 300s calc wind gust and mean wind speed
        settings.wind_gust = max(store_speeds)
        settings.wind_speed = statistics.mean(store_speeds)
        wind_dir_average = wind_direction_byo.get_average(store_directions)

        settings.wind_dir_average = wind_dir_average + 180.0 if wind_dir_average < 180 else wind_dir_average - 180.0

        settings.rainfall = settings.rain_count * settings.BUCKET_SIZE # the accumulated rainfall in the past 60 min
        settings.rainfalldaily = settings.rain_count_daily * settings.BUCKET_SIZE # the accumulated rainfall since midnight
        bme280_sensor.read_all();
        ground_temp = temp_probe.read_temp()
        settings.ds18b20_probe = ground_temp
        temp_diff = settings.ambient_temperature - settings.ds18b20_probe # calc difference between BME280 temp and probe

        print(settings.wind_speed, " km/h", settings.wind_gust, " km/h", settings.wind_dir_average, " deg", wind_dir_average, " deg", settings.rainfall, " mm", settings.rainfalldaily, " mm",  settings.goodmeasure, " good", settings.badmeasure, " bad" )
        logging.info('{}:{} {}:{} {}:{} {}:{} {}:{} {}:{}'.format("hourly rainfall",settings.rainfall,"daily rainfall",settings.rainfalldaily,"wind speed",settings.wind_speed,"probe temp",ground_temp,"bme temp",settings.ambient_temperature,"temp diff",temp_diff)) 
           
        log_all_sensors_byo.Upload_data();
        logging.info('uploaded to wunderground')  

        #print (store_directions) 

        # clear data    
        store_speeds = []
        store_directions = []
        settings.goodmeasure = 0
        settings.badmeasure = 0


while False:
    settings.wind_gust = 100
    settings.wind_speed = 2
    settings.wind_dir_average = 5
    settings.rainfall = 5
    settings.rainfalldaily = 50
    bme280_sensor.read_all();
    WU_upload.Upload_data(); # upload data
    time.sleep(10)

while False:
    t = threading.currentThread()

    for t in threading.enumerate():
        print(t)
        logging.info(t)
    print(threading.active_count())    
    logging.info(threading.active_count())

while False:
    ground_temp = temp_probe.read_temp()
    print(ground_temp, " degC")
    


