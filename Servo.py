import RPi.GPIO as GPIO
import psutil
import picamera
from static.py.correo import *
from static.py.rutas import *
import time

# El pin del GPIO que estará conectado al pin de PWM del servo.
PIN = 13

# Configuramos el pin del RPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

# El 2do parámetro es la frecuencia del ciclo en Hertz. El manual del SG90
# indica un periodo del ciclo de 20ms (0,02s), entonce la frecuencia es
# 1/0,02 = 50 Hz
servo = GPIO.PWM(PIN, 50)

# Iniciamos el PWM, colocando el servo en 0º. Para ello, debemos enviarle
# un pulso de 1.5ms de ancho. La librería de Python requiere especificar el
# 'duty cycle' ('ciclo de trabajo', el tiempo que el pulso estará en 1) en
# porcentaje del ciclo. 1.5ms de 20ms es el 7.5%
"""servo.start(0)

# Le damos un segundo para que se mueva


# Cambiamos el duty cycle para mover el servo completamente a la derecha, -90º.
# Para ello, el SG90 espera un pulso de 2ms = 10%. Cambiamos el duty cycle.
servo.ChangeDutyCycle(1)
time.sleep(1)
servo.ChangeDutyCycle(0)

servo.ChangeDutyCycle(7.5)
time.sleep(1)
servo.ChangeDutyCycle(0)

servo.ChangeDutyCycle(12.5)
time.sleep(1)
servo.ChangeDutyCycle(0)


# Detenemos el PWM y reseteamos los pins del RPi"""


servo.start(0)
fecha = datetime.datetime.now().strftime("%Y_%m_%d_at_%H_%M_%S")
with picamera.PiCamera() as camera:
    #camera.rotation = 180
    camera.resolution = (1280, 720)
    servo.ChangeDutyCycle(2)
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
    servo.stop()
