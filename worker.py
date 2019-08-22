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


def start(led):
    GPIO.output(led, GPIO.HIGH)  # Turn on


def stop(led):
    GPIO.output(led, GPIO.LOW)  # Turn off


def titulos():
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT idUser, start, end FROM eventos ORDER BY start ASC")
    data = mycursor.fetchall()
    data = [i for sub in data for i in sub]
    return data


def ganador(data):
    max = len(data)
    result = 0
    if max == 0:
        result = -1
    else:
        for i in range(0, max, 3):
            if (data[i+1] <= dt.datetime.now() < data[i+2]):
                result = data[i]
    return result


if __name__ == '__main__':
    pastUser = -2
    try:
        while True:
            user = ganador(titulos())
            if not (user == pastUser):
                pastUser = user
                if (user == -1):
                    stop(user1)
                    stop(user2)
                    stop(user3)
                    text = "ID: -1"
                    write_log(text, outPath, outName)
                if (user == 0):
                    start(user1)
                    start(user2)
                    start(user3)
                    text = "ID: 0 "
                    write_log(text, outPath, outName)
                if (user == 1):
                    start(user1)
                    stop(user2)
                    stop(user3)
                    text = "ID: " + str(user) + " "
                    write_log(text, outPath, outName)
                if (user == 2):
                    stop(user1)
                    start(user2)
                    stop(user3)
                    text = "ID: " + str(user) + " "
                    write_log(text, outPath, outName)
                if (user == 3):
                    stop(user1)
                    stop(user2)
                    start(user3)
                    text = "ID: " + str(user) + " "
                    write_log(text, outPath, outName)
            time.sleep(5)
            mydb.commit()
    finally:

        GPIO.cleanup()
