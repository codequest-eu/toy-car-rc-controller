from continuous_task import ContinuousTask
from multiprocessing import Queue
import time

class RouteSender(ContinuousTask):

    def __init__(self, command_executor, directions, initialized_queue=Queue()):
        ContinuousTask.__init__(self, True, initialized_queue)
        self.command_executor = command_executor
        self.directions = directions
        self.start_process()

    def handle_command(self):
        pass

    def run(self):
        direction = next(self.directions)
        if direction:
            (wait_time, turn) = direction
            time.sleep(wait_time / 1000.0)
            self.command_executor.make_turn(turn)

    def initialize(self):
        self.directions.initialize()

    def destroy(self):
        self.directions.destroy()
