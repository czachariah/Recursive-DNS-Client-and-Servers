import threading
import socket
import sys

# need to make sure that correct arguments are given: rsHostname, rsListenPort, tsListenPort
if len(sys.argv) != 4:
    print("ERROR: Need to include the correct amount of arguments")
    exit()

# get list of hostnames to look up
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
port = int(sys.argv[2])
rs_addr = socket.gethostbyname(sys.argv[1])

# connect to the server on local machine
server_binding = (rs_addr, port)
rs.connect(server_binding)

# send host names one by one
for x in listOfHostnames:
    message = x
    rs.send(message.encode('utf-8'))
    data_from_server = rs.recv(500)
    print("[C]: Data received from RS server: {}".format(data_from_server.decode('utf-8')))

    # this means that we need to connect to the TS server to try to find the IP
    if " - NS" in data_from_server:
        print("Need to connect to TS Server!")

# this message is to let the RS server know we are done trying to find IPs
message = "DONE"
rs.send(message.encode('utf-8'))
data_from_server = rs.recv(500)
print("[C]: Data received from RS server: {}".format(data_from_server.decode('utf-8')))

# close the client socket
rs.close()
exit()

# main
if __name__ == "__main__":
    t2 = threading.Thread(name='client')
    t2.start()