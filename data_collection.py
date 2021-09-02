# this is the final script

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

#set up camera, buttons, LEDs, and sensors:

# camera
camera = PiCamera()

# cycles the LEDs 
button_gray = Button(6, bounce_time=0.1) # pin 31

# begin collecting data
button_green  = Button(22, bounce_time=0.1) # pin 15

# stop collecting data 
button_red = Button(16, bounce_time=0.1) # pin 36

# capture an image file
button_yellow = Button(17, bounce_time=0.1) # pin 11

# shutdown Pi
button_black = Button(5, bounce_time=0.1) # pin 29

# LEDs used for location classification

green_led = LED(23) # pin 16
yellow_led = LED(26) # pin 37
blue_led = LED(25) # pin 22

# set LEDs to off
green_led.off()
yellow_led.off()
blue_led.off()

# move on to collecting sensor data - only true if an LED color has been selected
record_data = False

# initialize the state of the LED color 
label = 'initial'

# sensors
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

# shutdown function
def shutdown_pi():
    print("Shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

# for color sensor only
def bar_graph(read_value):
    scaled = int(read_value / 1000)
    return "[%5d] " % read_value + (scaled * "*")

# collect data
def log_data():
	with open("/home/pi/enviro_data.csv", "a") as log:
	
# while True:

		# need to be formatted here:
		temp = round(tem_hum_sensor.temperature, 3)
		hum = round(tem_hum_sensor.relative_humidity, 3)
		pressure = round(lps.pressure, 3)
		co_2 = sgp30.eCO2
		tvoc = sgp30.TVOC

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

		# location classification
		loc_class = label

		log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18}\n"
			.format(strftime("%Y-%m-%d %H:%M:%S"),
				temp, hum, pressure, 
				co_2, tvoc,
				uv_raw, amb_raw, uv_idx, lux,
				violet, indigo, blue, cyan, green, yellow, orange, red,
				loc_class))
	sleep(1)

# take a photo, save file with timestamp
def capture_image():
    #print("image captured")
    timestamp = datetime.datetime.now().isoformat()
    camera.capture('/home/pi/%s.jpg' % timestamp)

# control green button to start data collection 
def start_collecting():
    global record_data
    record_data = True

# red button - stop recording data from sensors
def stop_collecting():
    global record_data
    record_data = False

# choose location classification (by color of LED)
def cycle_label():
    global label

    if label == 'initial':
        green_led.on()
        label = 'green'
        #print(label)
    elif label == 'green':
        green_led.off()
        yellow_led.on()
        label = 'yellow'
        #print(label)
    elif label == 'yellow':
        yellow_led.off()
        blue_led.on()
        label = 'blue'
        #print(label)
        
    elif label == 'blue':
        blue_led.off()
        label = 'initial'
        #print(label)


#set action performed by buttons 
button_yellow.when_pressed = capture_image

button_green.when_pressed = start_collecting

button_red.when_pressed = stop_collecting

button_gray.when_pressed = cycle_label

button_black.when_pressed = shutdown_pi

# master while loop 
while True:


    if record_data == True and label != 'initial':
        log_data()