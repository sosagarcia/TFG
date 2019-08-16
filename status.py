import threading 
import time
import datetime
import Adafruit_DHT
import RPi.GPIO as GPIO
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="renato",
  passwd="renato12",
  database="flaskcontacts"
)

hPath = "/var/log/iot/hum/"
tPath = "/var/log/iot/tem/"
irPath = "/var/log/iot/ir/"
disPath = "/var/log/iot/dis/"

GPIO.setmode(GPIO.BOARD)


# Distance
 
GPIO_TRIGGER = 16
GPIO_ECHO = 18
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


#Mouvement

pir = 8 

GPIO.setup(pir, GPIO.IN) 

global_enabled = 0
#Interrupción
GPIO.add_event_detect(pir, GPIO.RISING, callback = Alarma)


#Humedad y Temperatura

sensor = Adafruit_DHT.DHT11
pin = 9
GPIO.setup(pin, GPIO.IN) 

#Leds de aviso
ledM = 12 
ledH = 36
ledT = 38
ledA = 40

GPIO.setup(ledM, GPIO.OUT)
GPIO.setup(ledH, GPIO.OUT)
GPIO.setup(ledT, GPIO.OUT)
GPIO.setup(ledA, GPIO.OUT)

#Valores de aviso

tempMax = 23
humMax = 60


def write_log(text, path, name):
	log = open(path + datetime.datetime.now().strftime("%d-%m-%Y") + name,"a")
	line = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + text + "\n"
	log.write(line)
	log.close()


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

    

def temphum():
    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
    return (humedad, temperatura)

def alarma ():
    global global_enable
    global_enable = 1



if __name__ == '__main__':
    try:
        while True:
            humedad, temperatura = temhum()
            distancia = distance()
            print (humedad)
            print (temperatura)
            print (distancia)

            if temperatura > tempMax:
                GPIO.output(ledT, True)
            else:
                GPIO.output(ledT, False)
            if humedad > humMax:
                GPIO.output(ledH, True)
            else:
                GPIO.output(ledH, False)  

    except KeyboardInterrupt:
                print("Measurement stopped by User")
                GPIO.cleanup()


""" write_log(str(distance), disPath, "_Distancia")

if humedad is not None and temperatura is not None:
		textoT = str(temperatura)
        textoH = str(humedad)
	else:
		textoT = 'Error al obtener la lectura del sensor'
        textoH = 'Error al obtener la lectura del sensor'
                
    write_log(textoT, tPath, "_Temperatura")
	write_log(textoH, hPath, "_Humedad") """
