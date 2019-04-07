

class SocketWrapperAI:
    def __init__(self, clientsocket, clientNumber, ai = None):
        self.clientSocket = clientsocket
        self.clientNumber = clientNumber
        self.ai = ai
        