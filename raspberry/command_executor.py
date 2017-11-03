import serial
import serial_port

def enum(**enums):
    return type('Enum', (), enums)

Status = enum(IDLE=b'I', REMOTE=b'R', LEARNING=b'L', AUTONOMOUS=b'A')

class CommandExecutor:

    def __init__(self):
        self.ser = serial.Serial(serial_port.available_name(), 9600)

    def change_status(self, status):
        print("Changing status to %s" % status)
        self.ser.write(status)
        self.ser.flush()

    def make_turn(self, value):
        # print("Turn %d" % value)
        self.send_int_command(b'T', value)

    def set_speed(self, value):
        print("Set speed %d" % value)
        self.send_int_command(b'S', value)

    def send_int_command(self, command, value):
        serialized = chr(value // 256) + chr(value % 256)
        self.ser.write(command + serialized.encode('utf-8'))
        self.ser.flush()
