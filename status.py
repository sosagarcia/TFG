import threading
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import psutil
from static.py.correo import *
from static.py.rutas import *


# Valores de aviso

tempMax = 25
humMax = 60

# Distance
GPIO_TRIGGER = 23
GPIO_ECHO = 24

GPIO.setmode(GPIO.BCM)


def alarmaCheck():
    iteration = 0
    maxIterations = 5
    while (iteration < maxIterations):
        distancia = distance()
        if (30.0 > distancia):
            GPIO.output(ledA, True)
            text = "Se ha registrado una alarma, la distancia es de " + \
                str(distancia) + " cm."
            write_log(text, aPath, aName)
            # feedback = sendEmail(
            # str(text), "monitycont@gmail.com", "Alarma Registrada")
            textD = str(distancia) + " cm."
            write_log(textD, disPath, dName)
            GPIO.output(ledA, False)
            iteration = 6
            break

        iteration += 1
        time.sleep(1)


def alarma(channel):
    GPIO.output(ledM, True)
    text = "Se ha detectado movimiento"
    write_log(text, irPath, irName)
    alarmaCheck()

    GPIO.output(ledM, False)


GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


# Mouvement

pir = 25

GPIO.setup(pir, GPIO.IN)
# Interrupción
GPIO.add_event_detect(pir, GPIO.RISING, callback=alarma)


# Humedad y Temperatura

sensor = Adafruit_DHT.DHT11
pin = 4
GPIO.setup(pin, GPIO.IN)

# Leds de aviso
ledM = 18
ledH = 16
ledT = 20
ledA = 21

GPIO.setup(ledM, GPIO.OUT)
GPIO.setup(ledH, GPIO.OUT)
GPIO.setup(ledT, GPIO.OUT)
GPIO.setup(ledA, GPIO.OUT)
GPIO.output(ledT, False)
GPIO.output(ledH, False)
GPIO.output(ledA, False)
GPIO.output(ledM, False)


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
    distance = "{0:.2f}".format(distance)
    distance = float(distance)
    return distance


def distanceW():

    while True:
        time.sleep(60)
        distancia = distance()
        text = str(distancia) + " cm."
        write_log(text, disPath, dName)


def temphum():
    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
    return (humedad, temperatura)


def temphumW():

    while True:
        time.sleep(15)
        humedad, temperatura = temphum()
        if humedad is not None and temperatura is not None and (humedad <= 100):
            textoT = str(temperatura) + " ºC"
            textoH = str(humedad) + " %"
            if temperatura > tempMax:
                GPIO.output(ledT, True)
            else:
                GPIO.output(ledT, False)
            if humedad > humMax:
                GPIO.output(ledH, True)
            else:
                GPIO.output(ledH, False)

        else:
            textoT = 'Error al obtener la lectura del sensor'
            textoH = 'Error al obtener la lectura del sensor'

        write_log(textoT, tPath, tName)
        write_log(textoH, hPath, hName)


def tempcpu():
    temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    cpusan = psutil.cpu_percent(interval=1, percpu=False)
    return (str(temp) + ' ºC', str(cpusan) + ' %')


def tempW():
    while True:
        time.sleep(5)
        temperatura, cpu = tempcpu()
        write_log(temperatura, cpuTPath, cpuTName)
        write_log(cpu, cpuPath, cpuName)


if __name__ == '__main__':
    t1 = threading.Thread(target=temphumW)
    t2 = threading.Thread(target=distanceW)
    t4 = threading.Thread(target=tempW)

    t1.setDaemon(True)
    t2.setDaemon(True)
    t4.setDaemon(False)

    t1.start()
    t2.start()
    t4.start()

    try:
        t1.join()
    finally:
        GPIO.output(ledT, False)
        GPIO.output(ledH, False)
        GPIO.output(ledA, False)
        GPIO.output(ledM, False)
        GPIO.cleanup()  # reset all GPIO
