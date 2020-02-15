import threading
import socket
import sys

# need to make sure that correct arguments are given: rsHostname, rsListenPort, tsListenPort
if len(sys.argv) != 4:
    print("ERROR: Need to include the correct amount of arguments")
    exit()

#get list of hostnames to look up
listOfHostnames = list()
try:
   file = open("PROJI-HNS.txt","r")
   for line in file:
       line = line.replace("\r", "").replace("\n", "")
       listOfHostnames.append(line)
except IOError:
    print("ERROR opening file: PROJI-HNS.txt")
    exit()
file.close()

# create a sockets to connect with both the RS and TS servers
try:
    rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[C]: Sockets have been created to connect with the RS and TS servers.")
except socket.error as err:
    print('Socket Open Error: {} \n'.format(err))
    exit()

# Define the port on which you want to connect to the rs server
port = 50000
localhost_addr = socket.gethostbyname(socket.gethostname())

# connect to the server on local machine
server_binding = (localhost_addr, port)
rs.connect(server_binding)

# Receive data from the server
#data_from_server = cs.recv(500)
#print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

#send hostnames one by one
for x in listOfHostnames:
    message = x
    rs.send(message.encode('utf-8'))
    data_from_server = rs.recv(500)
    print("[C]: Data received from RS server: {}".format(data_from_server.decode('utf-8')))

    if " - NS" in data_from_server:
        print("Need to connect to TS Server!")


message = "DONE"
rs.send(message.encode('utf-8'))
data_from_server = rs.recv(500)
print("[C]: Data received from RS server: {}".format(data_from_server.decode('utf-8')))

# close the client socket
rs.close()
exit()

if __name__ == "__main__":
    t2 = threading.Thread(name='client')
    t2.start()