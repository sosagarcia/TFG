from time import sleep
from picamera import PiCamera


def takePicture():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (2592, 1944)
    camera.framerate = 15
    camera.annotate_text = "Hello world!"
    camera.start_preview()
    for i in range(100):
        camera.annotate_text = "Brightness: %s" % i
        camera.brightness = i
        sleep(0.1)
    camera.stop_preview()


if __name__ == '__main__':
    takePicture()
