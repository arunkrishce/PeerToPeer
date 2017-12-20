

Environment : Windows

Files to be executed,
	server.py - Registration Server
	RSclient.py - Client for registration Server
	RFCServer.py - Server to server RFC requests 
	RFClient.py - Client to request RFCs
	
Step 1: Execute python server.py from command prompt

Step 2: Execute python Rsclient.py from command prompt

Enter the hostname. Peer name starts with uppercase. Ex: Peer0, Peer1 etc
Enter the port number. Ex: 65420,65421
Give the message type Ex: Register, Leave, PQuery, KeepAlive

Step 3: Execute RFCServer.py along with the Portnumber in which RFC server listens 
		and Hostnumber

Ex: RFCServer.py 65420 Peer5

Step 4: Execute RFClient.py from command prompt along with the Portnumber 
		to which RFC server wishes to connect.
		
Ex: RFClient.py 65420

Enter the peer's hostname. Peer name starts with uppercase Ex: Peer0, Peer1
Give the message type as RFCQuery, GetRFC.

If the user wants to download a specific RFC give the RFC number after selecting GetRFC

Note: Please find the RFC_Files folder that contains folders for each peer 
		Peer0, Peer1, Peer2, Peer3, Peer4, Peer5 with rfc_index inside it 