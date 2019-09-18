from RPi import GPIO
from time import sleep

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
servo.start(0)

# Le damos un segundo para que se mueva


# Cambiamos el duty cycle para mover el servo completamente a la derecha, -90º.
# Para ello, el SG90 espera un pulso de 2ms = 10%. Cambiamos el duty cycle.
servo.ChangeDutyCycle(1)
sleep(1)
servo.ChangeDutyCycle(0)

servo.ChangeDutyCycle(7.5)
sleep(1)
servo.ChangeDutyCycle(0)

servo.ChangeDutyCycle(12.5)
sleep(1)
servo.ChangeDutyCycle(0)


# Detenemos el PWM y reseteamos los pins del RPi
servo.stop()
GPIO.cleanup()
