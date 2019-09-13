from time import sleep
from picamera import PiCamera


def takePicture():
    camera = PiCamera()
    camera.rotation = 180
    camera.start_preview()
    sleep(5)
    camera.stop_preview()
    camera.start_preview(alpha=200)
    sleep(5)
    camera.stop_preview()


if __name__ == '__main__':
    takePicture()
