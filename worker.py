from datetime import date, datetime, timedelta
import datetime as dt
import mysql.connector
import time
import RPi.GPIO as GPIO
from static.py.rutas import *
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


switcher = {
    1: 13,
    2: 19,
    3: 26
}


def start(id):
    user = switcher.get(id, -1)
    switcher.get(id)
    text = "ID: " + str(id)
    print
    GPIO.output(user, GPIO.HIGH)  # Turn on
    write_log(text, outPath, outName)


def stop(id):
    user = switcher.get(id)
    GPIO.output(user, GPIO.LOW)  # Turn off


def titulos():
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT idUser, start, end FROM eventos ORDER BY start ASC")
    data = mycursor.fetchall()
    data = [i for sub in data for i in sub]
    return data


def ganador(data):
    max = len(data)
    result = list()
    if max == 0:
        return result
    else:
        for i in range(0, max, 3):
            if (data[i+1] <= dt.datetime.now() < data[i+2]):
                result.append(data[i])
    return result


if __name__ == '__main__':
    try:
        while True:
            user = ganador(titulos())
            # No hay ningún evento guardado aún
            if len(user) == 0:
                stop(1)
                stop(2)
                stop(3)
            else:
                for i in [1, 2, 3]:
                    if i in user:
                        start(i)
                    else:
                        stop(i)

            time.sleep(5)
            mydb.commit()
    finally:

        GPIO.cleanup()
