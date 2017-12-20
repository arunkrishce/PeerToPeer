import socket
import pickle
import pprint
import ast


class PeerData:
    def __init__(self, host=None, port=None, cookie=None):
        self.hname = host
        self.port = port
        self.cookie = cookie


class RegPeer:
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port


class NodePeer:
    def __init__(self, obj: RegPeer):
        self.peer_objt = obj
        self.next = None

    def setnext(self, newnext):
            self.next = newnext

    def setpeer_obj(self, obj: RegPeer):
        self.peer_objt = obj

    def getnext_peer(self):
        return self.next

    def peer_obj(self):
        return self.peer_objt


class PeerList:
    def __init__(self):
        self.head = None

    def add(self,peer):
        tem = NodePeer(peer)
        tem.setnext(self.head)
        self.head = tem
        print("Added to linked list")

    def display(self):
        tem = self.head
        while tem != None:
            peer_objt = tem.peer_obj()
            print(peer_objt.hname, peer_objt.port)
            tem = tem.getnext_peer()


recObj = PeerList()

HOST,PORT = '127.0.0.1', 64800
client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_conn.connect((HOST, PORT))
print("Enter host")
hname = input()
print("Enter the port number of the server between 65xxx-65xxx")
port = input()
print("Select the action to perform 1.Register '\n' 2.PQuery '\n' 3.Leave")
message = input()
name = hname+'.txt'
try:
    file = open(name,'r')
    peerInfo = ast.literal_eval(file.read())
    print(peerInfo)
    file.close()
    cookie = peerInfo.get('cookie','None')
    print(cookie)
except IOError:
    cookie = 'None'
sendMessage = 'GET ' + message + ' P2P/DI-1.1 <cr> <lf>\nHost ' + hname +' <cr> <lf>\nPort ' + str(port) +' <cr> <lf>\nCookie '+ str(cookie) +' <cr> <lf>\n<cr> <lf>'
print(sendMessage)
client_conn.send(sendMessage.encode('utf-8'))

if message == "Register":
    try:
        P0 = PeerData(hname,port)
        recvMessage =(client_conn.recv(2048).decode('utf-8'))
        print(recvMessage)
        P0.cookie = int(recvMessage[recvMessage.index('cookie')+len('cookie')+2:])
        print('Cookie information updated: Cookie is ', P0.cookie)
        print('Saving cookie in ' + hname + '.txt')
        attributes = vars(P0)
        name = hname+'.txt'
        file = open(name,'w')
        file.write(pprint.pformat(attributes))
        file.close()
    except:
        print('Already Registered')
    client_conn.close()
if message == 'PQuery':
        file = client_conn.makefile(mode='rb')
        recObj = pickle.load(file)
        print('Type of received object is ', type(recObj))
        print('Presenting the list of Active Peers')
        recObj.display()
        file.close()
        client_conn.close()
if message == 'Leave':
    print(client_conn.recv(2048).decode('utf-8'))
    client_conn.close()