import threading
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import psutil
import picamera
from static.py.correo import *
from static.py.rutas import *


# Valores de aviso

tempMax = 26
humMax = 30
disB = 30
disA = 85
alt = 100
email = "monitycont@gmail.com"


# Intervalo de muestreo

htTm = 15
disT = 60
cpuS = 5

linea = {
    "mail": "1",
    "tam": "2",
    "disB": "3",
    "disA": "4",
    "tem": "5",
    "hum": "6",
    "htTm": "7",
    "disT": "8",
    "cpuS": "9"

}

data = {
    "tem": tempMax,
    "hum": humMax,
    "disB": disB,
    "disA": disA,
    "tam": alt,
    "mail": email,
    "htTm": htTm,
    "disT": disT,
    "cpuS": cpuS

}


# Distance
GPIO_TRIGGER = 26
GPIO_ECHO = 25

GPIO.setmode(GPIO.BCM)


GPIO.setwarnings(False)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Humedad y Temperatura

sensor = Adafruit_DHT.DHT11
pin = 17
GPIO.setup(pin, GPIO.IN)

# Leds de aviso
ledM = 5
ledH = 20
ledT = 21
ledA = 4
motor = 13

GPIO.setup(ledM, GPIO.OUT)
GPIO.setup(ledH, GPIO.OUT)
GPIO.setup(ledT, GPIO.OUT)
GPIO.setup(ledA, GPIO.OUT)
GPIO.setup(motor, GPIO.OUT)
GPIO.output(ledT, False)
GPIO.output(ledH, False)
GPIO.output(ledA, False)
GPIO.output(ledM, False)
servo = GPIO.PWM(motor, 50)


def updateData():
    configs = read_conf()
    global tempMax
    global humMax
    global disB
    global disA
    global alt
    global email
    global htTm
    global disT
    global cpuS
    email = str(configs[1])
    alt = float(configs[2])
    disB = int(configs[3])
    disA = int(configs[4])
    tempMax = int(configs[5])
    humMax = int(configs[6])
    htTm = int(configs[7])
    disT = int(configs[8])
    cpuS = int(configs[9])


"""def alarmaCheck():
    disAlarma = float(give("dis"))
    iteration = 0
    maxIterations = 5
    while (iteration < maxIterations):
        distancia = distance()
        if (disAlarma > distancia):
            GPIO.output(ledA, True)
            text = "Se ha registrado una alarma, la distancia es de " + \
                str(distancia) + " cm."
            write_log(text, aPath, aName)
            email = give("mail")
            # feedback = sendEmail(
            # str(text), email, "Alarma Registrada")
            textD = str(distancia) + " cm."
            write_log(textD, disPath, dName)
            GPIO.output(ledA, False)
            iteration = 6
            break

        iteration += 1
        time.sleep(1)
"""


def takePicture():
    servo.start(0)
    fecha = datetime.datetime.now().strftime("%Y_%m_%d_at_%H_%M_%S")
    with picamera.PiCamera() as camera:
        #camera.rotation = 180
        camera.resolution = (1280, 720)
        servo.ChangeDutyCycle(1)
        time.sleep(1)
        servo.ChangeDutyCycle(0)
        # max resolution = (2592, 1944)

        #ruta2 = camara + fecha + ".jpg"
        time.sleep(0.5)
        # camera.capture(ruta2)
        ruta = images + fecha + "A"+".jpg"

        # SEGUNDA FOTO
        camera.capture(ruta)
        servo.ChangeDutyCycle(7.5)
        time.sleep(1)
        servo.ChangeDutyCycle(0)
        time.sleep(0.5)
        # camera.capture(ruta2)
        ruta = images + fecha + "B"+".jpg"
        camera.capture(ruta)
        # TERCERA FOTO
        servo.ChangeDutyCycle(12.5)
        time.sleep(1)
        servo.ChangeDutyCycle(0)
        time.sleep(0.5)
        # camera.capture(ruta2)
        ruta = images + fecha + "C"+".jpg"
        camera.capture(ruta)
        # servo.stop()


def alarma(channel):
    GPIO.output(ledM, True)
    takePicture()
    text = "Se ha detectado movimiento, Una foto ha sido tomada"
    write_log(text, irPath, irName)
    # alarmaCheck()
    email = give("mail")
    # feedback = sendEmail(
    # str(text), email, "Se ha detectado movimiento")
    time.sleep(2)
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
        time.sleep(disT)
        distancia = distance()
        actual = alt - distancia
        nivel = 1 / (alt / actual) * 100
        text = "{0:.2f}".format(nivel) + " %"
        if (nivel > 100) or (nivel < 0):
            text = text + "(Error de Calibración)"
        write_log(text, disPath, dName)
        avisos(nivel)


def avisos(actual):
    disA = int(give("disA"))
    disB = int(give("disB"))
    if disB > actual:
        GPIO.output(ledA, True)
        actualStr = "{0:.2f}".format(actual)
        text = "Nivel del Agua :" + \
            actualStr + " %"
        write_log(text, aPath, aName)
        email = give("mail")
        # feedback = sendEmail(
        # str(text), email, "El nivel del agua es muy BAJO")
        GPIO.output(ledA, False)
    if disA < actual:
        GPIO.output(ledA, True)
        actualStr = "{0:.2f}".format(actual)
        text = "Nivel del Agua :" + \
            actualStr + " %"
        write_log(text, aPath, aName)
        email = give("mail")
        # feedback = sendEmail(
        # str(text), email, "El nivel del agua es muy ALTO")
        GPIO.output(ledA, False)


def temphum():
    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
    return (humedad, temperatura)


def temphumW():

    while True:
        tempMax = int(give("tem"))
        humMax = int(give("hum"))
        time.sleep(htTm)
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


def sistem():
    while True:
        time.sleep(cpuS)
        temperatura, cpu = tempcpu()
        write_log(temperatura, cpuTPath, cpuTName)
        write_log(cpu, cpuPath, cpuName)


def give(tipo):
    try:
        configs = read_conf()
        position = linea.get(str(tipo))
        dato = configs[int(position)]
        return dato
    except:
        actual = data.get(str(tipo))
        return actual


if __name__ == '__main__':

    # Mouvement
    pir = 22

    GPIO.setup(pir, GPIO.IN)
    # Interrupción
    GPIO.add_event_detect(pir, GPIO.RISING, callback=alarma)

    t1 = threading.Thread(target=temphumW)
    t2 = threading.Thread(target=distanceW)
    t4 = threading.Thread(target=sistem)

    t1.setDaemon(True)
    t2.setDaemon(True)
    t4.setDaemon(True)

    try:
        updateData()
    except:
        pass

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
