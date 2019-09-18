import RPi.GPIO as GPIO  # Importamos la libreria RPi.GPIO
import time  # Importamos time para poder usar time.sleep

GPIO.setmode(GPIO.BCM)  # Ponemos la Raspberry en modo BOARD
GPIO.setup(19, GPIO.OUT)  # Ponemos el pin 21 como salida
# Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
p = GPIO.PWM(19, 50)
p.start(2)  # Enviamos un pulso del 7.5% para centrar el servo

try:
    while True:  # iniciamos un loop infinito
        time.sleep(2)
        # Enviamos un pulso del 4.5% para girar el servo hacia la izquierda
        p.ChangeDutyCycle(2)
        time.sleep(2)  # pausa de medio segundo
        # Enviamos un pulso del 10.5% para girar el servo hacia la derecha
        p.ChangeDutyCycle(7.5)
        time.sleep(2)  # pausa de medio segundo
        # Enviamos un pulso del 7.5% para centrar el servo de nuevo
        p.ChangeDutyCycle(14)
        p.ChangeDutyCycle(2) # pausa de medio segundo

except KeyboardInterrupt:  # Si el usuario pulsa CONTROL+C entonces...
    p.stop()  # Detenemos el servo
    GPIO.cleanup()  # Limpiamos los pines GPIO de la Raspberry y cerramos el script
