from time import sleep
from picamera import PiCamera


def takePicture():
    camera = PiCamera()
    camera.rotation = 180
    # max de fotos: 2592 x 1944, de video : 1920×1080
    # camera.contrast = i #para el contraste
    # camera.brightness = n para el brillo , 50 por defecto, un poco mas en entornos oscuros, un poco menos en entornos luminoso
    camera.resolution = (1920, 1080)
    camera.framerate = 15
    camera.annotate_text = "Hello world!"
    camera.start_recording('/home/pi/Desktop/video.h264')
    camera.brightness = 55

    for i in range(100):
        camera.annotate_text = "Contrast: %s" % i
        camera.contrast = i
        sleep(0.1)
    camera.stop_recording()


if __name__ == '__main__':
    takePicture()
