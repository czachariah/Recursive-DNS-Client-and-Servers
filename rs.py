import threading
import socket
import sys

# need to make sure that the port number is given as an argument
if len(sys.argv) != 2:
    print("ERROR: Need to include a listen port argument.")
    exit()

# function used to insert words into the data table
def insertIntoTable(count,word,table):
    for i in range(count):
        for j in range(3):
            if table[i][j] == ".":
                table[i][j] = word
                return

#store the URLs and IPs from PROJI-DNSRS.txt
DNSTable = []
count = 0

# get the number of lines in the DNS list
try:
    file = open("PROJI-DNSRS.txt", "r")
    for line in file:
        count = count + 1
except IOError:
    print("ERROR opening file: PROJI-DNSRS.txt")
    exit()

# create the table and initialize it
for i in range(count):
    DNSTable.append([])
    for j in range(3):
        DNSTable[i].append(".")

# seperate the lines into words and store each word into a list
dataList = list()
try:
   file = open("PROJI-DNSRS.txt","r")
   for line in file:
       for word in line.replace("\r", "").replace("\n", "").split():
           dataList.append(word)

except IOError:
    print("ERROR opening file: PROJI-DNSRS.txt")
    exit()
file.close()

# populate DNS Table with the list of words
for word in dataList:
    insertIntoTable(count, word, DNSTable)

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

found = False
#get list of hostnames to check for
while True:
    found = False
    data_from_client = csockid.recv(500)
    print("Connection recieved: {}".format(data_from_client.decode('utf-8')))

    if data_from_client == "DONE":
        msg = "Cancelling Connection ... "
        csockid.send(msg.encode('utf-8'))
        break

    for word in range(count-1):
        if data_from_client == DNSTable[word][0]:
            msg = DNSTable[word][0] + " " + DNSTable[word][1] + " " + DNSTable[word][2]
            csockid.send(msg.encode('utf-8'))
            found = True

    if not found:
        msg = DNSTable[count-1][0] + " " + DNSTable[count-1][1] + " " + DNSTable[count-1][2]
        csockid.send(msg.encode('utf-8'))



# receive messages from the client

#data_from_client = csockid.recv(500)
#print(data_from_client)

# send back how are you
#msg = "How are you buddy?"
#csockid.send(msg.encode('utf-8'))

# Close the server socket
ss.close()
exit()

if __name__ == "__main__":
    t1 = threading.Thread(name='server')
    t1.start()

