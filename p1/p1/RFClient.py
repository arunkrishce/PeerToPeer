# Python file to implement the Peer to Peer communication with GetRFC and RFCQuery methods

# Created for CSC573 - Project1

# Author hpalani and akrish12

import sys
import socket
import pickle
import csv
import os

serverHost = '127.0.0.1'
BUFFER_SIZE = 2048


# Class to maintain the RFC index (RFC number, RFC Title and hname of peer)
class PeerRFCIndex:
    def __init__(self, peer_rfc_no=None, rfc_title=None, peer_hname=None):
        self.rfc_no = peer_rfc_no
        self.title = rfc_title
        self.hname = peer_hname


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
            print(index.rfc_no, ',', index.title, ',', index.hname)
            temp = temp.getnext()

			
    def load_data(self):
        filepath = os.path.dirname(sys.argv[0]) + "\\RFC_Files\\" + hname
        duplicate = duplicate_function(self, filepath)
        temp = self.head
        with open(filepath + '\\rfc_index.csv', 'a') as csv_file:
            while temp != None:
                index = temp.getnode()
                
                if len(duplicate) == 0:
                    row = index.rfc_no + ',' + index.title + ',' + index.hname + '\n'
                    csv_file.write(row)
                else:
                    if index.hname in duplicate:
                       print('Already present')
                    else:
                       row = index.rfc_no + ',' + index.title + ',' + index.hname + '\n'
                       csv_file.write(row)
                temp = temp.getnext()
        csv_file.close()


def duplicate_function(objtrecv: PeerRFCList, filepath):
    peer_list1 = []
    peer_list2 = []
    duplicate = []
    with open(filepath + '\\rfc_index.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            peer_list1.append(row[2])
    file.close()
    temp = objtrecv.head
    while temp != None:
        index = temp.getnode()
        peer_list2.append(index.hname)
        temp = temp.getnext()
    set_peer1 = set(peer_list1)
    set_peer2 = set(peer_list2)
    for i in list(set_peer1):
        for j in range(len(list(set_peer2))):
            if i == list(set_peer2)[j]:
                duplicate.append(i)
    return duplicate


rfc_rcv = PeerRFCList()
print('Enter peer from your list of active peers')
serverPort = int(sys.argv[1])

print('Establishing connection with the RFC Server:', serverPort)
clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET-network is IPv4, SOCK_STREAM is TCP Socket
clientSock.connect((serverHost, serverPort))    # To connect with the RFC Server
print('Enter Hostname')
hname = input()
print('Select the action to perform: 1.RFCQuery  2.GetRFC')    # Two peer to peer communication functions
action = input()

# If the peer has requested to get RFC index from other peer
if action == 'RFCQuery':
  resp_message = 'GET ' + action + ' P2P/DI-1.1 <cr> <lf>\nHost ' + hname
  print(resp_message)
  clientSock.send(resp_message.encode('utf-8'))
  file = clientSock.makefile(mode='rb')
  rfc_rcv = pickle.load(file)
  print('RFCList is')
  rfc_rcv.show_rfc_list()
  file.close()
  rfc_rcv.load_data()

elif action == 'GetRFC':
  resp_message = 'GET ' + action + ' P2P/DI-1.1 <cr> <lf>\nHost ' + hname
  print(resp_message)
  clientSock.send(resp_message.encode('utf-8'))
  print('Enter RFC number to download')
  rfc_no = input()
  clientSock.send(rfc_no.encode('utf-8'))
  loc = os.path.dirname(sys.argv[0])+ "\\RFC_Files\\" + hname
  filename = 'rfc' + rfc_no + '.txt'
  f = open(loc + '\\' + filename, 'wb')
  while True:
    print('Data received')
    data = clientSock.recv(BUFFER_SIZE)
    print('data=%s', data)
    if not data:
      break
    f.write(data)
  f.close()
  print('RFC is obtained')
clientSock.close()

