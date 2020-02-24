import threading
import socket
import sys

# need to make sure that the port number is given as an argument
if len(sys.argv) != 2:
    print("[RS]: ERROR: Need to include a listen port argument.")
    exit()


# function used to insert words into the data table
def insertIntoTable(count,word,table):
    for i in range(count):
        for j in range(3):
            if table[i][j] == ".":
                table[i][j] = word
                return


# store the URLs and IPs from PROJI-DNSRS.txt
DNSTable = []
count = 0

# get the number of lines in the DNS list
try:
    file = open("PROJI-DNSRS.txt", "r")
    for line in file:
        count = count + 1
except IOError:
    print("[RS]: ERROR opening file: PROJI-DNSRS.txt")
    exit()

# create the table and initialize it
for i in range(count):
    DNSTable.append([])
    for j in range(3):
        DNSTable[i].append(".")

# separate the lines into words and store each word into a list
dataList = list()
try:
   file = open("PROJI-DNSRS.txt","r")
   for line in file:
       for word in line.replace("\r", "").replace("\n", "").split():
           dataList.append(word)

except IOError:
    print("[RS]: ERROR opening file: PROJI-DNSRS.txt")
    exit()
file.close()

# populate DNS Table with the list of words
for word in dataList:
    insertIntoTable(count, word, DNSTable)

# create the socket for the rs server
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[RS]: Server socket created")
except socket.error as err:
    print('[RS]: socket open error: {}\n'.format(err))
    exit()

# bind the socket to the port to listen for the client
server_binding = ('', int(sys.argv[1]))
ss.bind(server_binding)
ss.listen(1)
host = socket.gethostname()
print("[RS]: Server host name is {}".format(host))
localhost_ip = (socket.gethostbyname(host))
print("[RS]: Server IP address is {}".format(localhost_ip))
csockid, addr = ss.accept()
print ("[RS]: Got a connection request from a client at {}".format(addr))

found = False
# get list of host names to check for
while True:
    found = False
    data_from_client = csockid.recv(500)
    print("[RS]: Connection received. Looking up : {}".format(data_from_client.decode('utf-8')) + " ...")

    # this is the code from the client that tells this server that there are no more host names to look up
    if data_from_client == "DONE":
        msg = "Look up done. Cancelling Connection ... "
        csockid.send(msg.encode('utf-8'))
        break
    # look through the table and see if the RS server has the IP address for the host name
    for word in range(count-1):
        hostToCheck = DNSTable[word][0].lower()
        if data_from_client == hostToCheck:
            msg = DNSTable[word][0] + " " + DNSTable[word][1] + " " + DNSTable[word][2]
            csockid.send(msg.encode('utf-8'))
            found = True

    # message (host name of the TS server) to the client to look to the TS server to find the IP
    if not found:
        msg = DNSTable[count-1][0] + " " + DNSTable[count-1][1] + " " + DNSTable[count-1][2]
        csockid.send(msg.encode('utf-8'))

# Close the server socket
ss.close()
exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='RSserver')
    t1.start()

