from continuous_task import ContinuousTask
import time

class RouteSender(ContinuousTask):

    def __init__(self, command_executor, directions):
        ContinuousTask.__init__(self, True)
        self.command_executor = command_executor
        self.directions = directions
        self.start_process()

    def handle_command(self):
        pass

    def run(self):
        direction = next(self.directions)
        if direction:
            (wait_time, turn) = direction
            time.sleep(wait_time)
            #self.command_executor.make_turn(turn)
            print(direction)

