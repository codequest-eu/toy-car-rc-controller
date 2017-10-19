import string

class ReplayDirectionsProvider:

    def __init__(self, directory):
        self.directory = directory
        self.file = open('%s/log' % directory, 'r')
        self.last_timestamp = None

    def __del__(self):
        self.file.close()

    def __iter__(self):
        while True:
            line = self.file.readline()
            if not line:
                break
            timestamp, direction = line.strip().split('/')
            wait = timestamp - self.last_timestamp if self.last_timestamp else 0
            self.last_timestamp = timestamp
            yield (wait, direction)

