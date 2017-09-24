from abc import ABCMeta
from multiprocessing import Value, Queue
import signal

class ContinuousTask:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.terminator = Value('i', 0)
        self.queue = Queue()
        self.process = ContinuousProcess(self)
        self.process.start()

    def terminate(self):
        self.terminator.value = 1
        self.process.join()

    def terminated(self):
        return self.terminator.value == 1

    def get_command(self):
        if self.started:
            try:
                return queue.get_nowait()
            except Queue.Empty:
                return (None, None)
        else:
            return queue.get()

    @abstractmethod
    def handle_command(self):
        pass

    @abstractmethod
    def run(self):
        pass

class ContinuousProcess(Process):

        def __init__(self, task):
            Process.__init__(self)
            self.daemon = True
            self.task = task

        def run(self):
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            while not self.task.terminated():
                self.task.handle_command()
                self.task.run()
