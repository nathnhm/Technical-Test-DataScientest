import time

class Timer(object):

    def __init__(self):
        self.timer = 0

    def start(self):
        self.timer = time.time()
    
    def stop(self):
        self.timer = 0

    def reset(self):
        self.timer = time.time()
    
    def getTime(self):
        if self.timer:
            return time.time() - self.timer
        return 0