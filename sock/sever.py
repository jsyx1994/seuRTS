import socket

HOST = "127.0.0.1"
PORT = 9898
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error as err:
    print('Bind failed. Error Code : %s'%format(err))
s.listen(10)
print("Socket Listening")


while True:
   # establish a connection
   clientsocket,addr = s.accept()      

   print("Sever: Got a connection from %s" % str(addr))
    
   msg = 'Sever: Thank you for connecting'+ "\r\n"
   clientsocket.send(msg.encode('ascii'))
   clientsocket.close()



