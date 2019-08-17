from datetime import date, datetime, timedelta
import datetime as dt
import mysql.connector
import threading
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

user1 = 13
user2 = 19
user3 = 26

GPIO.setup(user1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(user2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(user3, GPIO.OUT, initial=GPIO.LOW)

mydb = mysql.connector.connect(
    host="localhost",
    user="renato",
    passwd="renato12",
    database="flaskcontacts"
)


def actualiza(sql):
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


def blink(led):
    while True:  # Run forever
        GPIO.output(led, GPIO.HIGH)  # Turn on
        time.sleep(1)  # Sleep for 1 second
        GPIO.output(led, GPIO.LOW)  # Turn off
        time.sleep(1)  # Sleep for 1 second


def titulos():

    ahora = dt.datetime.now()
    antes = ahora - timedelta(days=32)
    despues = ahora + timedelta(hours=1)
    antes = str(antes)
    despues = str(despues)
    sql = 'SELECT idUser, start, end FROM eventos WHERE (' + antes + \
        ' < start) and ( start <  ' + despues + ') '
    data = actualiza(str(sql))
    data = [i for sub in data for i in sub]
    return data


def ganador(data):
    print("La data es ", data)
    max = len(data)
    result = list()
    if max == 0:
        result.append(0)
    else:
        for i in range(0, max, 3):
            if (data[i+1] <= dt.datetime.now() < data[i+2]):
                result.append(data[i])
    return result


if __name__ == '__main__':

    t1 = threading.Thread(target=blink, args=[user1])
    t2 = threading.Thread(target=blink, args=[user2])
    t3 = threading.Thread(target=blink, args=[user3])

    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)

    user = ganador(titulos())

    t1.start()
    t2.start()
    t3.start()

    try:
        print("El usuario actual es ", user)
        t1.join()
        t2.join()
        t3.join()
    finally:

        GPIO.cleanup()