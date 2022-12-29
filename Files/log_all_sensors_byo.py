#!/usr/bin/python3
import requests
import settings

#humidity = 60.998
#ambient_temp = 23.456
#pressure = 1067.890
ground_temp = 16.345
wind_speed = 5.6129
wind_gust = 12.9030
wind_average = 180
#rainfall = 1.270


def pa_to_inches(pressure_in_pa):
    pressure_in_inches_of_m = pressure_in_pa * 0.02953
    return pressure_in_inches_of_m

def mm_to_inches(rainfall_in_mm):
    rainfall_in_inches = rainfall_in_mm * 0.0393701
    return rainfall_in_inches

def khm_to_mph(speed_in_kmh):
    speed_in_mph = speed_in_kmh * 0.621371
    return speed_in_mph

def degc_to_degf(temperature_in_c):
    temperature_in_f = (temperature_in_c * (9/5.0)) + 32
    return temperature_in_f
    
def calc_dew_point_degc(t_corr,h):
	# Calculate the dew point
    dew_point_degc = t_corr-(14.55+0.114*t_corr)*(1-(0.01*h))-((2.5+0.007*t_corr)*(1-(0.01*h)))**3-(15.9+0.117*t_corr)*(1-(0.01*h))**14
    #dew_point_degc = round(dew_point_degc)
    #dew_point_degc = int(dew_point_degc)
    return dew_point_degc
    
def Upload_data():
    # create a string to hold the first part of the URL
    WUurl = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"
    WU_station_id = "XXXX" # Replace XXXX with your PWS ID
    WU_station_pwd = "YYYY" # Replace YYYY with your Password
    WUcreds = "ID=" + WU_station_id + "&PASSWORD="+ WU_station_pwd
    date_str = "&dateutc=now"
    action_str = "&action=updateraw"

    humidity_str = "{0:.2f}".format(settings.humidity)
    #ambient_temp_str = "{0:.2f}".format(degc_to_degf(settings.ambient_temperature))
    ambient_temp_str = "{0:.2f}".format(degc_to_degf(settings.ds18b20_probe))
    pressure_str = "{0:.2f}".format(pa_to_inches(settings.pressure))
    
    rain_str = "{0:.2f}".format(mm_to_inches(settings.rainfall)) # the accumulated rainfall in the past 60 min
    raindaily_str = "{0:.2f}".format(mm_to_inches(settings.rainfalldaily)) # the accumulated rainfall since midnight
    winddir_str = "{0:.2f}".format(settings.wind_dir_average)
    windspeed_str = "{0:.2f}".format(khm_to_mph(settings.wind_speed)) # mph instantaneous wind speed
    windgust_str = "{0:.2f}".format(khm_to_mph(settings.wind_gust)) # mph current wind gust
    
    #dew_point_degc = calc_dew_point_degc(settings.ambient_temperature,settings.humidity)
    dew_point_degc = calc_dew_point_degc(settings.ds18b20_probe,settings.humidity)
    dewptf_str = "{0:.2f}".format(degc_to_degf(dew_point_degc))
    
    r= requests.get(
        WUurl +
        WUcreds +
        date_str +
        "&humidity=" + humidity_str +
        "&tempf=" + ambient_temp_str +
        "&baromin=" + pressure_str +
        "&rainin=" + rain_str +
        "&winddir=" + winddir_str +       
        "&windspeedmph=" + windspeed_str +   
        "&windgustmph=" + windgust_str +   
        "&dailyrainin=" + raindaily_str +
        "&dewptf=" + dewptf_str +
        action_str)
        
    #print(r)
    #t = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=XXXX&PASSWORD=YYYY&dateutc=now&humidity=27.95&tempf=100.87&baromin=29.42&rainin=0.00&winddir=150.48&windspeedmph=0.90&windgustmph=1.04&dailyrainin=0.00&action=updateraw"
    #r=requests.get(t)
    #print("Received " + str(r.status_code) + " " + str(r.text))


#t = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID=XXXX&PASSWORD=YYYY&dateutc=now&humidity=27.95&tempf=100.87&baromin=29.42&rainin=0.00&winddir=150.48&windspeedmph=0.90&windgustmph=1.04&dailyrainin=0.00&action=updateraw"
#r=requests.post(t)

#Upload_data();
