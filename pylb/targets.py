class Target:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __str__(self):
        return "{0}:{1}".format(self.host, self.port)
