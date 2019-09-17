from time import sleep
from picamera import PiCamera
import datetime
camara = "/var/log/iot/camera/"


def takePicture():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (2592, 1944)
    camera.start_preview()
    sleep(5)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    ruta = camara + fecha + ".jpg"
    camera.capture(ruta)
    camera.stop_preview()


if __name__ == '__main__':
    takePicture()
