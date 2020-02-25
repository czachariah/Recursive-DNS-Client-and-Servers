import threading
import socket
import sys
import os
# need to make sure that correct arguments are given: rsHostname, rsListenPort, tsListenPort
if len(sys.argv) != 4:
    print("ERROR: Need to include the correct amount of arguments")
    exit()

RSPortNum = int(sys.argv[2])
if RSPortNum <= 1023:
    print("ERROR: Need to make sure that the port numbers are > 1023")
    exit()

TSPortNum = int(sys.argv[3])
if TSPortNum <= 1023:
    print("ERROR: Need to make sure that the port numbers are > 1023")
    exit()

# open file]
dir_name = os.path.dirname(os.path.abspath(__file__))
resolved = os.path.join(dir_name, "RESOLVED" + "." + "txt")

if os.path.exists(resolved):
    os.remove(resolved)
f=open("RESOLVED.txt", "a+")


# function used to connect to the TS server for IP lookup
def lookUpInTS(hostToLookUp, TShostName, TSPort):

    # create socket to connect with TS server
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Socket created to connect to TS server.")
    except socket.error as err:
        print('Socket Open Error: {} \n'.format(err))
        exit()

    # already have port number, now just get the hostname
    ts_addr = socket.gethostbyname(TShostName)

    # connect to the server on the local machine
    TS_server_binding = (ts_addr,int(TSPort))
    ts.connect(TS_server_binding)
    print("[C]; Connected to the TS server.\n")

    # send TS the host name to look up
    message_to_send = hostToLookUp
    ts.send(message_to_send.encode('utf-8'))
    print("[C]: Sending host name " + message + " to TS server for IP lookup ...")

    data_from_TSserver = ts.recv(500)
    f.write(data_from_TSserver.decode('utf-8') + "\n")
    print("[C]: Data received from TS server: {}".format(data_from_TSserver.decode('utf-8')))

    # close the socket
    ts.close()


# function used to connect to the TS server for IP lookup
def closeTS(TShostName, TSPort):
    # create socket to connect with TS server
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('Socket Open Error: {} \n'.format(err))
        exit()

    # already have port number, now just get the hostname
    ts_addr = socket.gethostbyname(TShostName)

    # connect to the server on the local machine
    TS_server_binding = (ts_addr, int(TSPort))
    ts.connect(TS_server_binding)

    # send TS the host name to look up
    message_to_send = "DONE"
    ts.send(message_to_send.encode('utf-8'))

    data_from_TSserver = ts.recv(500)
    print("[C]: Data received from TS server: {}".format(data_from_TSserver.decode('utf-8')))

    # close the socket
    ts.close()

# get list of host names to look up
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
    print("[C]: Socket created to connect to RS server.")
except socket.error as err:
    print('Socket Open Error: {} \n'.format(err))
    exit()

# Define the port on which you want to connect to the rs server
port = int(sys.argv[2])
rs_addr = socket.gethostbyname(sys.argv[1])

# connect to the server on local machine
server_binding = (rs_addr, port)
rs.connect(server_binding)
print("[C]: Connected to RS server.\n")

TSHostName = "something"
# send host names one by one
for x in listOfHostnames:
    message = x.lower()
    rs.send(message.encode('utf-8'))
    print("[C]: Sending host name " + message + " to RS server for IP lookup ...")
    data_from_server = rs.recv(500)


    print("[C]: Data received from RS server: {}".format(data_from_server.decode('utf-8')))

    # this means that we need to connect to the TS server to try to find the IP
    if " NS" in data_from_server:
        print("[C]: Connecting to the TS Server ...")
        getTSHostName = list()

        for word in data_from_server.split():
            getTSHostName.append(word)

        TSHostName = getTSHostName[0]
        lookUpInTS(message, TSHostName, sys.argv[3])
    else:
        f.write(data_from_server.decode('utf-8')+ "\n")
    print("\n")

# this message is to let the RS server know we are done trying to find IPs
message = "DONE"
rs.send(message.encode('utf-8'))
data_from_server = rs.recv(500)
print("[C]: Data received from RS server: {}".format(data_from_server.decode('utf-8')))

# close the TS connection as well
closeTS(TSHostName, sys.argv[3])

# close the client socket
f.close()
rs.close()
exit()

# main
if __name__ == "__main__":
    t2 = threading.Thread(name='client')
    t2.start()
