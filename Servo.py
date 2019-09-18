import RPi.GPIO as GPIO  # Importamos la libreria RPi.GPIO
import time  # Importamos time para poder usar time.sleep

GPIO.setmode(GPIO.BCM)  # Ponemos la Raspberry en modo BOARD
GPIO.setup(13, GPIO.OUT)  # Ponemos el pin 21 como salida
# Ponemos el 13 en modo PWM y enviamos 50 pulsos por segundo
p = GPIO.PWM(13, 50)  # Enviamos un pulso del 7.5% para centrar el servo
izq = 2
cent = 7.5
der = 14
try:
      # iniciamos un loop infinito
    p.start(izq)

    time.sleep(1)
    p.stop()
    time.sleep(1)

    p.start(cent)
    time.sleep(1)
    p.stop()
    time.sleep(1)

    p.start(der)
    time.sleep(1)
    p.stop()
    time.sleep(1)

    # pausa de medio segundo
    # Enviamos un pulso del 10.5% para girar el servo hacia la derecha
    p.start(izq)
    time.sleep(.05)  # pausa de medio segundo
    # Enviamos un pulso del 7.5% para centrar el servo de nuevo
    # pausa de medio segundo
    p.stop()
except KeyboardInterrupt:  # Si el usuario pulsa CONTROL+C entonces...
    p.stop()  # Detenemos el servo
    GPIO.cleanup()  # Limpiamos los pines GPIO de la Raspberry y cerramos el script
