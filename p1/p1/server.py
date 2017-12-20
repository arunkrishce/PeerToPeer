# Python file to implement the Registration Server(RS) that maintains the Peer list data structure.

# Created for CSC573 - Project1

# Author hpalani and akrish12

import random
import time
import socket
import pickle
import platform


# Class that contains the record of each peer
class PeerData:
    def __init__(self, host=None, port_number=None, cookie=None):
        self.hname = host
        self.port = port_number
        self.flag_active = True
        self.cookie = cookie                                # Cookie assigned to the peer
        self.TTL = 7200                                     # TTL field
        self.recent_regtime = time.strftime("%H:%M:%S")     # Recent time/date the peer has registered
        if self.cookie == None:
            print('In None block')
            self.cookie = random.randint(1, 50)
            print(self.cookie)
            self.number_of_activetimes = 0
        else:
            self.cookie = cookie
            self.number_of_activetimes = calculate_instance(self.hname, peer_list)


# Class to maintain the list of Peers
class PeerList:
    def __init__(self):
        self.head = None

    def add(self, peer):
        temp = NodePeer(peer)
        temp.setnext(self.head)
        self.head = temp

    def display(self):
        temp = self.head
        while temp != None:
            peer_obj = temp.peer_obj()
            print("Peer object data", peer_obj.hname, peer_obj.port, peer_obj.cookie, peer_obj.flag_active, peer_obj.TTL
                  , peer_obj.number_of_activetimes, peer_obj.recent_regtime)
            temp = temp.getnext_peer()


# Class that maintains the pointer of various peers
class NodePeer:
    def __init__(self, obj: PeerData):
        self.peer_objt = obj
        self.next = None

    def peer_obj(self):
        return self.peer_objt

    def getnext_peer(self):
        return self.next

    def setpeer_obj(self, obj: PeerData):
        self.peer_objt = obj

    def setnext(self, newnext):
        self.next = newnext


# Function to check about the active peer list and peer that are in active state
def checkpeer_list(list: PeerList, host):
    peer_list1 = PeerList()
    check = check_peer(list, host)
    temp = list.head
    while temp != None:
        peer_obj = temp.peer_obj()
        if check == True and peer_obj.flag_active == True:
            print('Both are found')
            peer_list1.add(peer_obj)
            temp = temp.getnext_peer()
        elif check == True and peer_obj.flag_active == False:
            print('Peer Left recently.Please register again with cookie to get list of active peers')
            temp = temp.getnext_peer()
        else:
            print('Please register to get list of Peers')
            temp = temp.getnext_peer()
    peer_list1.display()
    return peer_list1


# When a peer leaves the system, the activity flag is changed to False or Inactive
def setinactive(host, list: PeerList):
    temp = list.head
    while temp != None:
        peer_obj = temp.peer_obj()
        if peer_obj.hname == host:   # The corresponding check is made before making the flag as inactive
            peer_obj.flag_active = False
            print('Flag is set to False')
            temp = temp.getnext_peer()
        else:
            temp = temp.getnext_peer()


# Function is used to calculate the number of times peer has been active
def calculate_instance(host, list: PeerList):
    temp = list.head
    while temp != None:
        peer_obj = temp.peer_obj()
        if peer_obj.hname == host:
            peer_obj.no_active += 1
            temp = temp.getnext_peer()
            return peer_obj.no_active
        else:
            temp = temp.getNext()
    return 0


# Function to check whether the peer has registered or not
def check_peer(list: PeerList, host):
    temp = list.head
    check = False
    if temp == None:
        print('No peer has registered')
    while temp != None:
        peer_obj = temp.peer_obj()
        if peer_obj.hname == host:
            check = True
            temp = temp.getnext_peer()
        else:
            temp = temp.getnext_peer()
    return check


serverName = ''
serverPort = 64800
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET - network is IPv4, SOCK_STREAM is TCP Socket
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # To avoid the Time Wait State
serverSocket.bind((serverName, serverPort))
serverSocket.listen(10)    # Accept 10 connections at a time

peer_list = PeerList()
activepeer_list = PeerList()
while True:
    client_connection, client_address = serverSocket.accept()
    response_message = client_connection.recv(2048).decode('utf-8')         # Fetching host, port and cookie
    host = response_message[response_message.index('Host') + len('Host')               # info from the response message
                            + 1: response_message.index(' <cr> <lf>\nPort')]
    port = response_message[response_message.index('Port') + len('Port')
                            + 1: response_message.index(' <cr> <lf>\nCookie')]
    Cookie = response_message[response_message.index('Cookie') + len('Cookie')
                              + 1: response_message.index(' <cr> <lf>\n<cr> <lf>')]

    # Check if the peer wants to register and perform corresponding activities
    if "Register" in response_message:
        if Cookie == 'None':
            print('Creating an object without cookie')
            peer_obj = PeerData(host, port)  # Peer object without cookie
        else:
            peer_obj = PeerData(host, port, Cookie)  # Peer object with cookie
            activepeer_list = checkpeer_list(peer_list, host)

        if check_peer(activepeer_list, host) == True:
            client_connection.close()
        else:
            peer_list.add(peer_obj)
            peer_list.display()
            print('Peer registration successful')
            response_message = "P2P-DI/1.0 200 OK" + "\r\n" + \
                               "Date: " + time.strftime("%H:%M:%S") + "\r\n" + \
                               "OS: " + platform.platform() + "\r\n" + \
                               "cookie: " + str(peer_obj.cookie)
            client_connection.send(response_message.encode('utf-8'))
            client_connection.close()

    # To cater the request from client to know about the list of active peers
    elif "PQuery" in response_message:
        peer_list.display()
        activepeer_list = checkpeer_list(peer_list, host)
        if activepeer_list.head != None:
            print('Sending the linked list')                        # List that has active peers
            client_connection.send(pickle.dumps(activepeer_list, pickle.HIGHEST_PROTOCOL))  # To use highest protocol
        client_connection.close()

    # If a peer wants to leave from the system, the following statements are executed and flag is set to inactive
    elif "Leave" in response_message:
        setinactive(host, peer_list)
        peer_list.display()
        client_connection.send("You have left the system".encode('utf-8'))
        client_connection.close()

