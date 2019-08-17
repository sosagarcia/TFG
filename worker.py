from datetime import date, datetime, timedelta
import datetime as dt
import mysql.connector
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
    try:
        while True:
            user = ganador(titulos())
            print(user)
            if (user == 0):
                stop(user1)
                stop(user2)
                stop(user3)
            if (user == 1):
                start(user1)
                stop(user2)
                stop(user3)
            if (user == 2):
                stop(user1)
                start(user2)
                stop(user3)
            if (user == 3):
                stop(user1)
                stop(user2)
                start(user3)
            time.sleep(5)
    finally:

        GPIO.cleanup()
