import mysql.connector
import threading
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
        sleep(1)  # Sleep for 1 second
        GPIO.output(led, GPIO.LOW)  # Turn off
        sleep(1)  # Sleep for 1 second


if __name__ == '__main__':

    t1 = threading.Thread(target=blink, args=[user1])
    t2 = threading.Thread(target=blink, args=[user2])
    t3 = threading.Thread(target=blink, args=[user3])

    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)

    t1.start()
    t2.start()
    t3.start()

    while True:
        print("Hello")
