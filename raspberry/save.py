import os
from glob import glob
from picamera import PiCamera
from time import sleep
import serial
import time
from multiprocessing import Process
import signal

term = False

def timestamp():
	return int(round(time.time() * 1000))

def filenames():
    frame = 0
    while True:
        yield 'images/%d.jpg' % timestamp()

def soft_kill(signum, frame):
    print("signal received\n")
    term = True

def capture():
    with PiCamera(resolution=(640, 480), framerate=15) as camera:
        camera.start_preview()
        sleep(2)
        camera.capture_sequence(filenames(), use_video_port=True)

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

for file in glob("images/*.jpg"):
    os.remove(file)

p = Process(target=capture)
p.start()

signal.signal(signal.SIGINT, soft_kill)

ser = serial.Serial('/dev/ttyACM0',9600)
print("read serial communication")
with open("log", "w") as f:
    while not term:
        read_serial = ser.readline()
        f.write(str(timestamp()) + "/" +  read_serial)

print("terminating\n")
print(p.pid)
kill(p.pid)

