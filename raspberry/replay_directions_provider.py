import string

class ReplayDirectionsProvider:

    def __init__(self, directory):
        self.directory = directory
        self.log_file = open('%s/log' % directory, 'r')
        self.last_timestamp = None

    def __del__(self):
        self.log_file.close()

    def __iter__(self):
        return self

    def next(self):
        line = self.log_file.readline()
        if not line:
            raise StopIteration()
        timestamp, direction = map(int, line.strip().split('/'))
        wait = timestamp - self.last_timestamp if self.last_timestamp else 0
        self.last_timestamp = timestamp
        return (wait, direction)
   
    def __next__(self):
        return self.next()

