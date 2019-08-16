#!/usr/bin/python

import RPi.GPIO as GPIO
import datetime
import time
log_path = "/var/log/iot/ir/"
GPIO.setmode(GPIO.BOARD) #Set GPIO to pin numbering
pir = 8 #Assign pin 8 to PIR
led = 12 #Assign pin 10 to LED
GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input
GPIO.setup(led, GPIO.OUT) #Setup GPIO pin for LED as output

time.sleep(2) #Give sensor time to startup

def write_log(text):
	log = open(log_path + datetime.datetime.now().strftime("%d-%m-%Y") + "_Movimiento.log","a")
	line = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + text + "\n"
	log.write(line)
	log.close()

try:
	while True:
		if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
			write_log("Movimiento detectado!")
			GPIO.output(led, True) #Turn on LED
			time.sleep(6) #Keep LED on for 4 seconds
			GPIO.output(led, False) #Turn off LED
			time.sleep(1)

except Exception,e: #Ctrl+c
	write_log(str(e))
	GPIO.output(led, False)

finally:
	GPIO.output(led, False) #Turn off LED in case left on
	GPIO.cleanup() #reset all GPIO
