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

GPIO.setmode(GPIO.BCM) 


def alarma (channel):
    global global_enable
    global global_distance 
    global_distance = 1
    
    print ("Se ha detectado movimiento")
    GPIO.output(ledA, True)



# Distance
 
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

global_distance = 20.0


#Mouvement

pir = 25

GPIO.setup(pir, GPIO.IN) 

global_enabled = 0
#Interrupción
GPIO.add_event_detect(pir, GPIO.RISING, callback = alarma)


#Humedad y Temperatura

sensor = Adafruit_DHT.DHT11
pin = 4
GPIO.setup(pin, GPIO.IN) 

#Leds de aviso
ledM = 18
ledH = 16
ledT = 20
ledA = 21

GPIO.setup(ledM, GPIO.OUT)
GPIO.setup(ledH, GPIO.OUT)
GPIO.setup(ledT, GPIO.OUT)
GPIO.setup(ledA, GPIO.OUT)

#Valores de aviso

tempMax = 25
humMax = 70



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

def distanceW():
    try:
        while True:
            distancia = distance()
            print (distancia)
            time.sleep(global_distance) 
    except KeyboardInterrupt:
	    # Registra el error en el archivo log y termina la ejecucion
	    print("Measurement stopped by User")
  

def temphum():
    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
    return (humedad, temperatura)

def temphumW():
    try:
        while True:
            humedad, temperatura = temphum()
            print (humedad)
            print (temperatura)
    
            if temperatura > tempMax:
                GPIO.output(ledT, True)
            else:
                GPIO.output(ledT, False)
            if humedad > humMax:
                GPIO.output(ledH, True)
            else:
                GPIO.output(ledH, False)
            time.sleep(10)     
    
    except KeyboardInterrupt:
	    # Registra el error en el archivo log y termina la ejecucion
	    print("Measurement stopped by User")
        GPIO.output(ledT, False)
        GPIO.output(ledH, False)



if __name__ == '__main__':

    t1 = threading.Thread(target=temphumW)
    t2 = threading.Thread(target=distanceW)
    t1.start()
    t2.start()



""" write_log(str(distance), disPath, "_Distancia")

if humedad is not None and temperatura is not None:
		textoT = str(temperatura)
        textoH = str(humedad)
	else:
		textoT = 'Error al obtener la lectura del sensor'
        textoH = 'Error al obtener la lectura del sensor'
                
    write_log(textoT, tPath, "_Temperatura")
	write_log(textoH, hPath, "_Humedad") """
