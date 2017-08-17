import os
from glob import glob
from picamera import PiCamera
from time import sleep
import serial
import time
from multiprocessing import Process, Value
import signal
import sys

global camera_process
global serial_process
global terminated 

def timestamp():
    return int(round(time.time() * 1000))

def filenames():
    frame = 0
    while terminated.value == 0:
        yield 'images/%d.jpg' % timestamp()

def capture():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    with PiCamera(resolution=(640, 480), framerate=15) as camera:
        camera.start_preview()
        sleep(2)
        camera.capture_sequence(filenames(), use_video_port=True)

def read_serial():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    ser = serial.Serial('/dev/ttyACM0', 9600)
    with open("log", "w") as f:
        while terminated.value == 0:
            read_serial = ser.readline()
            f.write(str(timestamp()) + "/" +  read_serial)

def interrupt_handler(signal, frame):
    terminated.value = 1

def cleanup():
    try:
        os.remove("log")
        for file in glob("images/*.jpg"):
            os.remove(file)
    except OSError:
        pass

# main

terminated = Value('i', 0)

camera_process = Process(target=capture)
camera_process.daemon = True

serial_process = Process(target=read_serial)
serial_process.daemon = True

cleanup()
camera_process.start()
serial_process.start()

signal.signal(signal.SIGINT, interrupt_handler)

camera_process.join()
serial_process.join()
