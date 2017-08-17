class InterruptHandler:

    def __init__(self, terminator):
        self.terminator = terminator

    def __call__(self, signal, frame):
        self.terminator.value = 1

    
