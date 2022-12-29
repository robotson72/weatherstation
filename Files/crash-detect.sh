#!/bin/sh
while true; do
  echo starting weather program - Current Date and Time is: `date +"%Y-%m-%d %T"`>> /home/pi/weather-station/log.txt  
  python3 /home/pi/weather-station/weather_station_byoV6.py &
  wait $!
  sleep 10
done
exit
