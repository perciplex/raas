import time

class Hardware:
    def __init__(self, name):
        self.name = name
        self.last_heartbeat = time.time() - 1000 # initialize to a time a while ago

    def heartbeat(self):
        self.last_heartbeat = time.time()

    def is_alive(self):
        return (time.time() - self.last_heartbeat) < 10. # dead if 10 seconds have passed since last heartbeat