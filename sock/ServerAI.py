import socket
import json
from hardCodedJSON import UnitTypeTable, UnitType, GameState

# @author: Jiawei, Y.
# Main file to look at.
# Methods you should look at:
#       BabyAI.getAction(player, gs)
#       policy(player, gs)
# Currently, policy always returns "Do nothing until be killed."
# For the details "parameter" and "type" in the return dict of 
# policy, please check hardCodedJSON.py

class ServerAI:
    """
    Python Version server.

    This is nothing more than a simple python implementation of ``Runserverexample.java``.

    serverAI creates a socket to listen to the given address and call ``SocketWrapperAI``
    for handling communication.

    Parameters
    ----------
    ``serverSocket`` : socket, optional default None.
        The serverSocket for channeling.
        Initialize the server socket by this parameters.
    
    ``host`` : string, optional default '127.0.0.1'.
    
    ``port`` : int, optional default '9898'.

    ``ai`` : object, optional default None.
        The ``AI`` used in server side.

    ``DEBUG`` : int, optional default '1'.
        The debug parameter.
        Print intermediate process when set to '1'
    """


    DEBUG = 1

    def __init__(self, serverSocket = None,
                 host = '127.0.0.1', port = 9898, ai=None):
        self.socketAddr = (host,port)
        self.ai = ai
        if serverSocket is None:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.serverSocket = serverSocket
    
    def runServer(self):
        """
        run the server

        Parameters
        ----------
        self: object

        Returns
        -------
        None
        """
        if self.DEBUG >=1 : print('Server is runing')
        clientNumber = 0
        self.serverSocket.bind(self.socketAddr)
        self.serverSocket.listen(10)
        
        try:
            while True:
                print('waiting for a connection')
                clientSocket, clientAddress= self.serverSocket.accept()
                SocketWrapperAI(clientSocket,clientNumber,self.ai)
        finally:
            self.serverSocket.close()


class SocketWrapperAI:
    """
    Python Version SocketWrapperAI.

    SocketWrapperAI handle with welcome messages and acknowledgements between clients and server, 
    as well as passing the game state information to the ``AI`` used in this server.

    Parameters
    ----------
    ``DEBUG``: int, optional default '1'.
        The debug parameter.
        Print intermediate process when set to '1'
    
    ``utt``: object, optional default None.
        ``UnityTypeTable``

    ``ai``: object, optional default None.
        ``AI``

    All of the remaining parameters will be passed through serverAI, don't worry it.
    
    Notes
    ---------
    This is nothing more than a simple python implementation of ``JSONRunserverexample.java``.
    However, some internal implementation details is different from santi's one.
    """

    DEBUG = 1
    def __init__(self, clientsocket, clientNumber, ai = None):
        self.clientSocket = clientsocket
        self.clientNumber = clientNumber
        # utt: UnityTypeTable
        self.utt = None
        self.ai = ai
        if self.DEBUG >= 1: print("New connection with client# {} at {}".format(clientNumber,clientsocket))
        self.run()

    def run(self):
        """
        If you don't understand the main logic behind santi's work, 
        please carefully go through the comments of this function.
        """
        try:
            welcome = 'PyJSONSocketWrapperAI: you are client #%i\n'%self.clientNumber
            self.clientSocket.sendall(welcome.encode())
            while True:
                # retrieve the message from socket
                msg = str(self.clientSocket.recv(10240).decode())

                # connection broken, retry.
                if msg == 0:
                    break

                # client closes the connection.
                elif msg.startswith('end'):
                    self.clientSocket.close()
                    exit(self)

                # budget initialization
                elif msg.startswith('budget'):
                    msg = msg.split()
                    self.ai.reset()
                    self.ai.timeBudget = int(msg[1])
                    self.ai.iterationsBudget = int(msg[2])
                    if self.DEBUG >= 1: 
                        print("setting the budget to: {},{}".format(self.ai.timeBudget,self.ai.iterationsBudget))
                    # send back ack
                    self.clientSocket.sendall('ack\n'.encode()) 

                # utt initialization
                elif msg.startswith('utt'):
                    
                    msg = msg.split('\n')[1]

                    # json.loads() returns dict
                    self.utt = json.loads(msg)

                    # reset ai with current utt
                    self.ai.reset(self.utt)
                    if self.DEBUG >= 1: 
                        print('setting the utt to: {}'.format(self.utt))
                        pass
                    
                    # send back ack
                    self.clientSocket.sendall('ack\n'.encode()) 


                # client asks server to return units actions for current game state
                elif msg.startswith('getAction'):
                    # get player ID
                    player = msg.split()[1]
                    # get game state
                    gs = msg.split('\n')[1]
                    if self.DEBUG >= 1: 
                        print('getAction for player {}'.format(player))
                        print('with game state %s'%gs)
                    # json.loads() returns dict
                    gs = json.loads(gs)
                    # call ai.getAction to return the player actions ##string##
                    pa = self.ai.getAction(player,gs)

                    # send the encoded player actions string to client
                    self.clientSocket.sendall(('%s\n'%pa).encode()) 

                    if self.DEBUG >= 1: 
                        print('action sent!')

                # get preGameAnalysis
                elif msg.startswith('preGameAnalysis'):
                    print('get preGameAnalysis, it has not been implemented yet')
                    pass

                elif msg.startswith('gameOver'):
                    msg = msg.split()
                    winner = msg[1]
                    if self.DEBUG >= 1: 
                        print('gameOver %s'%winner)
                    self.ai.gameOver(winner)
                    self.clientSocket.sendall(('ack\n').encode()) 
                    self.clientSocket.close()
        finally:
            self.clientSocket.close()
            print('Connection with client# {} closed'.format(self.clientNumber))


class BabyAI:
    def __init__(self,utt = None, policy = None):
        self.timeBudget = 100
        self.iterationsBudget = 0
        self.utt = utt
        self.actions = {}
        self.policy = policy

    def reset(self,utt=None):
        self.utt = utt
        return 
    
 
    def getAction(self, player, gs):
        """Compute the MLP loss function and its corresponding derivatives
        with respect to the different parameters given in the initialization.

  
        Parameters
        ----------
        ``player`` : int. 
            Denotes current player.

        ``gs`` : dict, Game state data.
             {'time': int, 'pgs':{...}}


        Returns
        -------
        ``msg`` : string, unitActions to send back.
            '["unitID":int, "unitAction":{"type": int, "parameter": int, "unitType": str}]'
            

        Examples
        --------
        ``gs``:

            {'time': 0, 
             'pgs': {'width': 8, 
                     'height': 8, 
                     'terrain': '0000000000000000000000000000000000000000000000000000000000000000', 
                     'players': [{'ID': 0, 'resources': 5}, 
                                 {'ID': 1, 'resources': 5}], 
                     'units':   [{'type': 'Resource', 'ID': 0, 'player': -1, 
                                  'x': 0, 'y': 0, 'resources': 20, 'hitpoints': 1
                                 }, 
                                 {'type': 'Resource',  'ID': 1,  'player': -1, 
                                  'x': 7,  'y': 7,  'resources': 20, 'hitpoints': 1
                                 }, 
                                 {'type': 'Base', 'ID': 2, 'player': 0, 
                                  'x': 2, 'y': 1, 'resources': 0, 'hitpoints': 10
                                 }, 
                                 {'type': 'Base', 'ID': 3, 'player': 1, 
                                  'x': 5, 'y': 6, 'resources': 0, 'hitpoints': 10
                                 }]}, 
             'actions': []
            }


        ``msg``: string

        [
            { "unitID":4, 
              "unitAction":{"type": 2, "parameter": 0}
            },
            { "unitID":6, 
              "unitAction":{"type": 1, "parameter": 1}
            },
            { "unitID":8, 
              "unitAction":{"type": 1, "parameter": 2}
            }
            { "unitID":2, 
              "unitAction":{"type":4, "parameter":0, "unitType":"Worker"}
        ]
        """
        msg = '['


        '''
        policy returns dict:
            {id:{type':int, 'isAttack':boolean, 'x':int, 'y':int, 'parameter':int, 'unitType':string}}

        Note: the return of policy differs from getAction
        '''
        self.actions = policy(player, gs)



        first = True
        for unit,unitAction in self.actions:
            if first == False:
                msg = msg + ' ,'
            if unitAction['isAttack'] == True:
                msg = msg + '{"unitID":{}, "unitAction":{"type":{}, "x":{},"y":{}}'.format(unit, unitAction['type'],unitAction['x'],unitAction['y'])
            else:
                msg = msg + '{"unitID":{}, "unitAction":{"type":{}, "parameter":{}, "unitType":"{}"}'.format(unit, unitAction['type'],unitAction['parameter'],unitAction['unitType'])
            
            first = False
        
        msg = msg + ']'


        return msg


    def gameOver(self,winner):
        print('winner: ',winner)
        return



def policy(player, gs):
    """Policy used to generate actions.

  
        Parameters
        ----------
        ``player`` : int. 
            Denotes current player.

        ``gs`` : dict, Game state data.
             {'time': int, 'pgs':{...}}


        Returns
        -------
        ``unitsActions`` : dict, unitActions to send back.
            {id:{type':int, 'isAttack':boolean, 'x':int, 'y':int, 'parameter':int, 'unitType':string}}
            

        Examples
        --------
        ``gs``:

            {'time': 0, 
             'pgs': {'width': 8, 
                     'height': 8, 
                     'terrain': '0000000000000000000000000000000000000000000000000000000000000000', 
                     'players': [{'ID': 0, 'resources': 5}, 
                                 {'ID': 1, 'resources': 5}], 
                     'units':   [{'type': 'Resource', 'ID': 0, 'player': -1, 
                                  'x': 0, 'y': 0, 'resources': 20, 'hitpoints': 1
                                 }, 
                                 {'type': 'Resource',  'ID': 1,  'player': -1, 
                                  'x': 7,  'y': 7,  'resources': 20, 'hitpoints': 1
                                 }, 
                                 {'type': 'Base', 'ID': 2, 'player': 0, 
                                  'x': 2, 'y': 1, 'resources': 0, 'hitpoints': 10
                                 }, 
                                 {'type': 'Base', 'ID': 3, 'player': 1, 
                                  'x': 5, 'y': 6, 'resources': 0, 'hitpoints': 10
                                 }]}, 
             'actions': []
            }


        ``unitsActions``: dict
            { 3: {'type': 0, 'isAttack': False, 'x': 0, 'y': 0, 'parameter': 0, 'unitType':'Worker'},
              5: {'type': 1, 'isAttack': False, 'x': 0, 'y': 0, 'parameter': 2, 'unitType':'Worker'},
              7: {'type': 5, 'isAttack': True, 'x': 3, 'y': 8, 'parameter': 0, 'unitType':'Ranged'},
            }
    """
    # gs is a json string
    # get all the units of current player
    units = []
    enemyUnits = []
    resources = []
    unitsActions = {}
    tmpDic = {'type':0 , 'isAttack':False, 'x':0, 'y':0, 'parameter':0, 'unitType':'default'}


    for unit in gs['pgs']['units']:
        # get resources
        if unit['player'] == -1:
            resources.append(unit)
        else:
            # get all the units of current player
            if unit['player'] == player:
                units.append(unit)
                tmpDic['unitType'] = unit['type']

                # assign actions to all the units of current player
                unitsActions[unit['ID']] = tmpDic
            else:
                # get enemyUnits
                enemyUnits.append(unit)
    
    return unitsActions
    




if __name__ == "__main__":
    babyAI = BabyAI()
    serverAI = ServerAI(ai=babyAI)
    serverAI.runServer()
                
