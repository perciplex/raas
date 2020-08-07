import time


class Hardware:
    """
    Class for maintaining hardware state
    """

    def __init__(self, name):
        self.name = name
        self.last_heartbeat = time.time() - 1000  # initialize to a time a while ago

    def heartbeat(self):
        self.last_heartbeat = time.time()

    def starting_job(self):
        self.last_heartbeat = time.time() + 120  # give it two minutes to do its job

    def is_alive(self):
        return (
            time.time() - self.last_heartbeat
        ) < 10.0  # dead if 10 seconds have passed since last heartbeat
