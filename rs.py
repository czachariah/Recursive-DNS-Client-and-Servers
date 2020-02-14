import threading
import time
import socket
import sys

# need to make sure that the port number is given as an argument
if len(sys.argv) != 2:
    print("ERROR: Need to include a listen port argument.")
    exit()

# create the socket for the rs server
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[S]: Server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()

# bind the socket to the port to listen for the client
server_binding = ('', int(sys.argv[1]))
ss.bind(server_binding)
ss.listen(1)
host = socket.gethostname()
print("[S]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[S]: Server IP address is {}".format(localhost_ip))
csockid, addr = ss.accept()
print ("[S]: Got a connection request from a client at {}".format(addr))

# send a intro message to the client.
msg = "Welcome to CS 352!"
csockid.send(msg.encode('utf-8'))

data_from_client = csockid.recv(500)
print(data_from_client)



# Close the server socket
ss.close()
exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='server')
    t1.start()