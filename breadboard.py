# What this does:
# 1. Use the gray button to cycle through 3 LEDs (green, yellow, blue) - assigns a color to the location class
# 2. Use the black button to take a photo with the Pi Camera
# 3. Use the green button to start the function "some action" which currently prints the word "hello" every second
# 4. Use the red button to stop printing "hello"

from gpiozero import LED, Button, LEDBoard
from signal import pause
import time
import datetime 
from picamera import PiCamera

camera = PiCamera()

# cycles the LEDs 
button_gray = Button(6, bounce_time=0.1) # pin 31

# begin collecting data
button_green  = Button(22, bounce_time=0.1) # pin 15

# stop collecting data 
button_red = Button(16, bounce_time=0.1) # pin 36

# capture an image file
button_black = Button(17, bounce_time=0.1) # pin 11

green_led = LED(23) # pin 16
yellow_led = LED(26) # pin 37
blue_led = LED(25) # pin 22

# set LEDs to off
green_led.off()
yellow_led.off()
blue_led.off()

# move on to collecting sensor data
record_data = False

# # initialize the state of the LED color 
label = 'initial'

# define an action that the green buttons starts and the red button ends
# this will be the sensor data collection function
# right now it is just a dummy function that prints "Some Data"

def some_action():
    #collect data from sensors and record it to a CSV file
    print(label, "Some Data")
    time.sleep(1)
           
# take a photo, save file with timestamp
def capture_image():
    print("image captured")
    timestamp = datetime.datetime.now().isoformat()
    camera.capture('/home/pi/%s.jpg' % timestamp)

def start_collecting():
    global record_data
    record_data = True

def stop_collecting():
    global record_data
    record_data = False

def cycle_label():
    global label

    if label == 'initial':
        green_led.on()
        label = 'green'
        print(label)
    elif label == 'green':
        green_led.off()
        yellow_led.on()
        label = 'yellow'
        print(label)
    elif label == 'yellow':
        yellow_led.off()
        blue_led.on()
        label = 'blue'
        print(label)
        
    elif label == 'blue':
        blue_led.off()
        label = 'initial'
        print(label)


#capture an image each time black button is pressed
button_black.when_pressed = capture_image

button_green.when_pressed = start_collecting

button_red.when_pressed = stop_collecting

button_gray.when_pressed = cycle_label

while True:


    if record_data == True and label != 'initial':
        some_action()
    
