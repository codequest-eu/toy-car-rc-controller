import abc
from multiprocessing import Value, Queue, Process
import queue as BaseQueue
import signal

class ContinuousTask:
    __metaclass__ = abc.ABCMeta

    def __init__(self, started):
        self.terminator = Value('i', 0)
        self.started = started
        self.queue = Queue()

    def start_process(self):
        self.process = ContinuousProcess(self)
        self.process.start()

    def terminate(self):
        self.terminator.value = 1
        self.queue.put(('exit', None))
        self.process.join()

    def terminated(self):
        return self.terminator.value == 1

    def get_command(self):
        if self.started:
            try:
                return self.queue.get_nowait()
            except BaseQueue.Empty:
                return (None, None)
        else:
            return self.queue.get()

    @abc.abstractmethod
    def handle_command(self):
        pass

    @abc.abstractmethod
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
