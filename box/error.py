''' box - error.py '''

class SSHError(Exception):
    ''' Constructor for SSH connection related errors '''

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return str(self.message.decode())
