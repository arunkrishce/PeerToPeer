import pickle
import csv
import threading
import sys
import os
import socket

Host = ''
print(sys.argv[0])
port = int(sys.argv[1])
hname = sys.argv[2]
BUFFER_SIZE = 256


class Peer(threading.Thread):
    def __init__(self, socket, client_ip):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        print(self.lock)
        self.client_socket = socket
        self.ip = client_ip[0]
        self.socket = client_ip[1]

    def run(self):
        print("Received connection request from:" + threading.currentThread().getName())
        recvText = self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
        print(recvText)
        Host = recvText[recvText.index('Host ')+5:]
        loc = os.path.dirname(sys.argv[0])+ "\\RFC_Files\\" + hname
        if 'GetRFC' in recvText:
            numbrfc = self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
            print(numbrfc)
            fname = 'rfc' + numbrfc + '.txt'
            try:
                f = open(loc+'\\' + fname,'rb')
            except:	
                print('Unable to open file.Error')
                self.client_socket.close()
            l = f.read(BUFFER_SIZE)
            while(l):
                self.client_socket.send(l)
                print('sent',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
            self.client_socket.close()
            print('Finished sending file')


        elif 'RFCQuery' in recvText:
            RFCIndexList = PeerRFCList()
            with open(loc+'\\rfc_index.csv','r') as f:
                read = csv.reader(f)
                for row in read:
                    print(row)
                    index = PeerRFCIndex(row[0],row[1],row[2])
                    RFCIndexList.add_rfc_list(index)
            f.close()

            if RFCIndexList.head != None:
                self.lock.acquire()
                self.client_socket.send(pickle.dumps(RFCIndexList, pickle.HIGHEST_PROTOCOL))
                self.lock.release()
                self.client_socket.close()

# Class to maintain the RFC index (RFC number, RFC Title and hname of peer)
class PeerRFCIndex:
    def __init__(self, peer_rfc_no=None, rfc_title=None, peer_hname=None):
        self.rfc_no = peer_rfc_no
        self.title = rfc_title
        self.hname = peer_hname

    def getnumbrfc(self):
        return self.rfc_no

    def getheading(self):
        return self.title

    def gethname(self):
        return self.hname


class PeerRFCNode:
    def __init__(self, objt: PeerRFCIndex):
        self.peer_rfc_node = objt
        self.next = None

    def getnode(self):
        return self.peer_rfc_node

    def setnode(self, objt: PeerRFCIndex):
        self.peer_rfc_node = objt

    def getnext(self):
        return self.next

    def setnext(self, newnext):
        self.next = newnext


class PeerRFCList:
    def __init__(self):
        self.head = None

    def add_rfc_list(self, index):
        temp = PeerRFCNode(index)
        temp.setnext(self.head)
        self.head = temp
        print('Peer index added to list')

    def show_rfc_list(self):
        temp = self.head
        while temp != None:
            index = temp.getnode()
            print(index.peer_rfc_no, ',', index.rfc_title, ',', index.hname)
            temp = temp.getnext()


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((Host, port))
threads = []

while True:
    serverSocket.listen(6)
    print('listening')
    clientSocket, client_ip = serverSocket.accept()
    print(clientSocket)
    print(client_ip)
    new_peer=Peer(clientSocket, client_ip)
    print("NEw peer")
    new_peer.start()
    print("peer start")
    threads.append(new_peer)
    for t in threads:
        t.join()