from time import sleep, strftime, time
import csv
import datetime 
import board
import adafruit_ahtx0 # temp + hum
import adafruit_ltr390 # UV + amb light
import adafruit_lps2x # temp + pressure
import adafruit_sgp30 # air quality sensor
from adafruit_as7341 import AS7341 # color sensor
from gpiozero import LED, Button, LEDBoard
from signal import pause
from picamera import PiCamera
import subprocess

# set up buttons and sensors:

# sensors:
i2c = board.I2C()

# AHT20 temp and humidity sensor 
tem_hum_sensor = adafruit_ahtx0.AHTx0(i2c)

# LPS22 Temp and Barometric Pressure sensor
lps = adafruit_lps2x.LPS22(i2c)

# AS7341 color sensor
color_sensor = AS7341(i2c)

# LTR 390 UV/Ambient Light Sensor
ltr = adafruit_ltr390.LTR390(i2c)

# SPG 30 air quality sensor
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8AAE)

# shutdown button
button_grey = Button(5, bounce_time=0.1) 

# button to grab one data point
button_blue = Button(26, bounce_time=0.1)

# shutdown function
def shutdown_pi():
    print("Shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

def record_one_datapoint():
# collect data
    with open("/home/pi/enviro_test_data.csv", "a") as log:
    
        # need to be formatted here:
        temp = round(tem_hum_sensor.temperature, 3)
        hum = round(tem_hum_sensor.relative_humidity, 3)
        pressure = round(lps.pressure, 3)
        tvoc = sgp30.TVOC
        
        uv_idx = round(ltr.uvi, 3)
        lux = round(ltr.lux, 3)

        # color sensors:
        violet = color_sensor.channel_415nm
        indigo = color_sensor.channel_445nm
        blue = color_sensor.channel_480nm
        cyan = color_sensor.channel_515nm
        green = color_sensor.channel_555nm
        yellow = color_sensor.channel_590nm
        orange = color_sensor.channel_630nm
        red = color_sensor.channel_680nm

        # log the collected data into a csv file

        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}\n"
            .format(strftime("%Y-%m-%d %H:%M:%S"),
                temp, hum, pressure, 
                tvoc, uv_idx, lux,
                violet, indigo, blue, cyan, green, yellow, orange, red))

while True:

    button_blue.when_pressed = record_one_datapoint

    button_grey.when_pressed = shutdown_pi  



    

