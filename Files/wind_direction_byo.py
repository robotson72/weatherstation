from gpiozero import MCP3008
import time
import math
import settings
adc = MCP3008(channel=0)
count = 0
values = []
settings.goodmeasure = 0
settings.badmeasure = 0


# N on wind vane is pointing NORTH
# 0 deg = wind coming from south, pointer is pointing NORTH
# 90 deg = wind coming from west, pointer is pointing EAST
# 180 deg = wind coming from north, pointer is pointing SOUTH
# 270 deg = wind coming from east, pointer is pointing WEST

volts = {0.4: 0.0,
		 1.3: 22.5, # was 1.4
		 1.2: 45.0,
		 2.8: 67.5,
		 2.7: 90.0,
		 2.9: 112.5,
		 2.2: 135.0,
		 2.5: 157.5,
		 1.8: 180.0,
		 2.0: 202.5,		 
		 0.7: 225.0,
		 0.8: 247.5,
		 0.1: 270.0,
		 0.3: 292.5,
		 0.2: 315.0,
		 0.6: 337.5}		 

def get_average(angles):
	
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    s = sin_sum / flen
    c = cos_sum / flen
    arc = math.degrees(math.atan(s / c))
    average = 0.0

    if s > 0 and c > 0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360

    return 0.0 if average == 360 else average

def get_value(length):
	data = []
	print("Measuring wind direction for %d seconds..." % length)
	start_time = time.time()
	
	while time.time() - start_time <= length: # while loop executes for time period length
		wind=round(adc.value*3.3,1)
		if not wind in volts: # keep only good measurements
			#print('unknown value ' + str(wind)+' ' + str(adc.value*3.3) )
			pass # no op
			settings.badmeasure = settings.badmeasure + 1
			
		else:
			data.append(volts[wind])
			settings.goodmeasure = settings.goodmeasure + 1
			
	return get_average(data)
		
while False: # for testing
		wind=round(adc.value*3.3,1)
		if not wind in volts: # keep only good measurements
			print('unknown value ' + str(wind)+' ' + str(adc.value*3.3) )
		else:
			print('found ' + str(wind) + ' ' + str(volts[wind])+' ' + str(adc.value*3.3))			
		time.sleep(1)



