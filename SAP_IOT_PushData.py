
'''
Created on 26.04.2017

This program reads sensor data from the GrovePI sensor kit on a Raspberry PI 3
and pushes the data into the SAP Cloud Platform IoT Services 4.0.

It needs to be run with Python 3 interpreter and the script needs to be
placed under following path on your Raspberry PI:

/home/pi/Desktop/GrovePi/Software/Python

@author: Matthias Allgaier, SAP SE
'''
import requests
import json
import time
import math
import time
import grovepi

# Definition of the message type for sensor data including initial values 
[valueTemp, valueLight, valueUltrasonic, valueSound, valueRotary, valueActivity] = [10, 20, 30, 40, 50, 60]

'''
Sensor & Measure Definitions
====================================
Sensor 1: Temperature -> Slot D2
Sensor 2: Light -> Slot A1
Sensor 3: Ultrasonic -> Slot D4
Sensor 4: Sound -> Slot A2
Sensor 5: Rotary -> Slot A0
Sensor 6: Activity / Humidity -> Slot D2

Note: field "activity" (can also be used as a custom field)
'''

# D2 (Combined sensor for temperature and humidity)
# Blue sensor (Version 1.2)
sensor_temperature = 2
blue = 0    

# A1
sensor_light = 1

# D4
sensor_ultrasonic = 4

# A2
sensor_sound= 2

# A0
sensor_rotary = 0


# Time inetravll for polling the sensor data 
timeIntervall = 5

while True:
    
    try:
        print("")
        print("============================================")
        print("Reading sensor data ...")
        
             
        # Read light
        valueLight = grovepi.analogRead(sensor_light)
        print("Light value = %d" %valueLight)

        # Read ultrasonic
        valueUltrasonic = grovepi.ultrasonicRead(sensor_ultrasonic)
        print("Ultrasonic value = %d" %valueUltrasonic)
        
        # Read sound
        valueSound = grovepi.analogRead(sensor_sound)
        print("Sound value = %d" %valueSound)
                        
        # Read rotary
        valueRotary = grovepi.analogRead(sensor_rotary)
        print("Rotary value = %d" %valueRotary)

        # Read temperature & humiditiy 
        [temp,humidity] = grovepi.dht(sensor_temperature,blue)  
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            valueTemp = temp
            valueActivity = humidity
            print("Temperature value = %d" %valueTemp)
            print("Hummidity value = %d" %valueActivity)

        '''
        Create the HTTP POST message and send it to the SAP IoT service
        Adjust MAC address in the URL according to your physical node in the IoT service
        and fill it at the end with '0000'

        Example:
        ========
    
        MAC adress without '-' or ':' b827eb9d3f4c
        URL: https://ekt3.hcp.iot.sap/iot/gateway/rest/measures/b827eb9d3f4c0000'

        '''        
        data = json.dumps({"measureIds":[1,2,3,4,5,6], "values":[valueTemp,valueLight,valueUltrasonic,valueSound,valueRotary,valueActivity],"profileId":1600,"logNodeAddr":1})
        headers = {'content-type': 'application/json'}
        r = requests.post('https://aes-canary.hcp.iot.sap/iot/gateway/rest/measures/b827eb68d5eb0000',
        data=data, headers = headers,cert='keyStore.pem', timeout=5)
        responseCode = r.status_code
        print ("==> HTTP Response: %d" %responseCode)

        # wait some time to read again sensor values
        time.sleep(timeIntervall)
        
    except IOError:
        print ("Error")
       
