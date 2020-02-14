import threading
import time
import socket

try:
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Client socket created")
except socket.error as err:
    print('socket open error: {} \n'.format(err))
    exit()

# Define the port on which you want to connect to the server
port = 50000
localhost_addr = socket.gethostbyname(socket.gethostname())

# connect to the server on local machine
server_binding = (localhost_addr, port)
cs.connect(server_binding)

# Receive data from the server
data_from_server = cs.recv(500)
print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

message = "hello there"
cs.send(message.encode('utf-8'))






# close the client socket
cs.close()
exit()

if __name__ == "__main__":
    t2 = threading.Thread(name='client')
    t2.start()