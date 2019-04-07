import socket
from hardCodedJSON import UnitType,UnitTypeTable




class SocketAI:
    def __init__(self,
                 unitTypeTable,
                 sock = None,
                 host = '127.0.0.1',
                 port = 9898,
                 TIME_BUDGET = 100,
                 ITERATIONS_BUDGET = 0,
                 DEBUG = 1):
        self.utt = unitTypeTable
        self.socketAddr = (host,port)
        self.timeBudget = TIME_BUDGET
        self.iteratationsBudget = ITERATIONS_BUDGET
        self.debug = DEBUG
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
    
    def connect(self):
        self.sock.connect(self.socketAddr)
        welcome = self.sock.recv(1024)
        
        if welcome is not None:
            if self.debug >= 1:
                print ("Msg from Sever: "+welcome.decode())
                print ("SocketAI: welcome message received")
            self.reset()

    def reset(self):
        budgetInfo = 'budget %i %i\n'%(self.timeBudget,self.iteratationsBudget)
        self.sock.sendall(budgetInfo.encode())
        if self.debug >= 1: print('SocketAI: budgetd sent, waiting for ack')
        # wait for ack;
        ack = self.sock.recv(1024)
        if self.debug >= 1: print('SocketAI: ack received')

        # send the utt
        initConfig = 'utt\n' + UnitTypeTable.toJSON(self.utt) + '\n'
        self.sock.sendall(initConfig.encode())
        if self.debug >= 1: print('SocketAI: UTT sent, waiting for ack')

        # wait for ack
        ack = self.sock.recv(1024)
        if self.debug >= 1: print('SocketAI: ack received')

    def getAction(self, player, gs):
        # send the game state
        msg = 'getAction {}\n'.format(player)
        msg = msg + gs.toJSON() + '\n'
        self.sock.sendall(msg.encode())
        
        # wait to get an action
        actionString = self.sock.recv(10240).decode()
        if self.debug >= 1: print("action received from server: " + actionString)
        
        # pa = policy(player,gs,utt)
        pa = None
        return pa

        
        




if __name__ == "__main__":
    utt = UnitTypeTable()
    ai = SocketAI(utt)
    ai.connect()
    





