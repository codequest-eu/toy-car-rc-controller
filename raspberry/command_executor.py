import serial

def enum(**enums):
    return type('Enum', (), enums)

Status = enum(IDLE=b'I', REMOTE=b'R', LEARNING=b'L', AUTONOMOUS=b'A')

class CommandExecutor:

	def __init__(self):
		self.ser = serial.Serial('/dev/ttyACM0', 9600)

    def change_status(self, status):
    	self.ser.write(status)

    def make_turn(value):
    	serialized = chr(value / 256) + chr(value % 256)
    	self.ser.write(b'T' + serialized)
