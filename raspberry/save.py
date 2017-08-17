import os
from multiprocessing import Value
import signal
import time
from capturer import Capturer
from serial_reader import SerialReader
from interrupt_handler import InterruptHandler


def timestamp():
    return int(round(time.time() * 1000))

def start_capturing():
    directory = "session-%d" % timestamp()
    images = "%s/images" % directory
    os.makedirs(images)
    terminator = Value('i', 0)
   
    capturer = Capturer(directory, terminator)
    serial_reader = SerialReader(directory, terminator)
    
    capturer.start()
    serial_reader.start()

    return ([capturer, serial_reader], terminator)

if __name__ == "__main__":
    (processes, terminator) = start_capturing()
    signal.signal(signal.SIGINT, InterruptHandler(terminator))
    for process in processes:
        process.join()
