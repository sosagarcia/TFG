from datetime import date, datetime, timedelta
import datetime as dt
import mysql.connector
import time
import RPi.GPIO as GPIO
from static.py.rutas import *
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

user1 = 1
user2 = 2
user3 = 3

pinA = 23
pinB = 18
pinC = 24


switcher = {
    user1: pinA,
    user2: pinB,
    user3: pinC
}
while True:

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="renato",
            passwd="renato12",
            database="flaskcontacts"
        )
        break
    except:
        hoy = dt.datetime.now()
        print("Aun no ha sido posible conectar con la base de datos" +
              hoy.strftime("%d-%m-%Y_%H:%M:%S"))
        time.sleep(1)
        continue


def updateTaps():

    global switcher
    global user1
    global user2
    global user3
    global pinA
    global pinB
    global pinC
    user = switcher.get(1)
    print(user)
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT idPropietario, pin FROM tap")
    tap = mycursor.fetchall()
    print(tap)
    tap = [i for sub in tap for i in sub]
    user1 = tap[0]
    pinA = tap[1]
    user2 = tap[2]
    pinB = tap[3]
    user3 = tap[4]
    pinC = tap[5]
    user = switcher.get(1)
    switcher = {
        user1: pinA,
        user2: pinB,
        user3: pinC
    }
    GPIO.setup(pinA, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pinB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pinC, GPIO.OUT, initial=GPIO.LOW)


def start(id):
    user = switcher.get(id)
    led_is_on = GPIO.input(user)
    if not led_is_on:
        text = "ID: " + str(id)
        GPIO.output(user, GPIO.HIGH)  # Turn on
        write_log(text, outPath, outName)


def stop(id):
    user = switcher.get(id)
    led_is_on = GPIO.input(user)
    if led_is_on:
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
            updateTaps()
            user = ganador(titulos())
            # No hay ningún evento guardado aún
            if len(user) == 0:
                stop(user1)
                stop(user2)
                stop(user3)
            else:
                for i in [user1, user2, user3]:
                    if i in user:
                        start(i)
                    else:
                        stop(i)

            time.sleep(3)
            mydb.commit()
    finally:

        GPIO.cleanup()
