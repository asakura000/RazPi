# What this does:
# Creates/opens the csv file called 'enviro-data.csv'
# writes (adds) a new line of data to the csv file every second
# the data recorded are:
# 		temperature, humidity, barometric pressure, color sensor values, UV index, ambient light
# must add air quality

from time import sleep, strftime, time
import csv
import datetime 
import board
import adafruit_ahtx0 # temp + hum
import adafruit_ltr390 # UV + amb light
import adafruit_lps2x # temp + pressure
from adafruit_as7341 import AS7341 # color sensor

# Create sensor objects, communicating over the board's default I2C bus
# uses board.SCL and board.SDA
i2c = board.I2C()

# AHT20 temp and humidity sensor 
tem_hum_sensor = adafruit_ahtx0.AHTx0(i2c)

# LPS22 Temp and Barometric Pressure sensor
lps = adafruit_lps2x.LPS22(i2c)

# AS7341 color sensor
color_sensor = AS7341(i2c)

# for color sensor only
def bar_graph(read_value):
    scaled = int(read_value / 1000)
    return "[%5d] " % read_value + (scaled * "*")

# UV/Ambient Light Sensor
ltr = adafruit_ltr390.LTR390(i2c)

with open("/home/pi/enviro_data.csv", "a") as log:
	
# while True:

	# need to be formatted here:
	temp = round(tem_hum_sensor.temperature, 3)
	hum = round(tem_hum_sensor.relative_humidity, 3)
	pressure = round(lps.pressure, 3)

	# see documentation for explanation:
	# https://learn.adafruit.com/adafruit-ltr390-uv-sensor/python-circuitpython
	uv_raw = round(ltr.uvs, 3)
	amb_raw = round(ltr.light, 3)
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

	log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15}\n"
		.format(strftime("%Y-%m-%d %H:%M:%S"),temp, hum, pressure,
			uv_raw, amb_raw, uv_idx, lux,
			violet, indigo, blue, cyan, green, yellow, orange, red))
sleep(1)
	


