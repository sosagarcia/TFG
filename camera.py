from time import sleep
from picamera import PiCamera


def takePicture():
    camera = PiCamera()
    camera.rotation = 180
    camera.start_preview()
    sleep(2)
    camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()
    # camera.start_preview(alpha=200) es la trasmparencia


if __name__ == '__main__':
    takePicture()
