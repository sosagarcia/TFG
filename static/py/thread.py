import threading 
import time
import datetime
import Adafruit_DHT
import RPi.GPIO as GPIO

log_path = "/var/log/iot/ht/"
pin = 4

def write_log(text):
	log = open(log_path + datetime.datetime.now().strftime("%d-%m-%Y") + "_HumTemp.log","a")
	line = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + text + "\n"
	log.write(line)
	log.close()