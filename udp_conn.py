import struct
import hashlib
import socket
from urllib.parse import urlparse, urlencode
import os
from datetime import datetime
import time
from random import randint
DEFAULT_CONNECTION_ID = 0x41727101980
CONNECT = 0
TRANSACTION_ID = 1234567
class udp_conn:

	def __init__(self,t,tracker_list):
		self.torrent = t
		self.trackers = tracker_list
		self.protocol_id = DEFAULT_CONNECTION_ID
		self.log_file = open(t.log_file_name + ".txt", "a")


	def connection_udp(self):
		self.log_file.write("\n connect to udp tracker \n")
		connection_response = self.get_connect_msg() 
		action,trasaction_id,connection_id = struct.unpack("!LLQ",connection_response)
		self.log_file.write("\n" + "connection_id:"+ str(connection_id) + "\n")
		self.log_file.write("TRANSACTION_ID:" + str(TRANSACTION_ID))
		if(trasaction_id == 123456 and action == 0):
			announce_response = self.connect_to_tracker(connection_id)
			action, transaction_id, interval = struct.unpack('!3I',announce_response[:12])
			bin_peers = announce_response[20:]
			self.log_file.write("UDP CONNECTION SUCCESSFULL \n")
			self.log_file.write("--------------------------------- \n")
			self.log_file.close()
			return bin_peers
			
			





	def get_connect_msg(self):
		action = CONNECT	
		trasaction_id = 123456
		message = struct.pack("!QLL",self.protocol_id,action,trasaction_id)
		
		return self.send_msg(message)



	def connect_to_tracker(self,connection_id):
		my_peer_id = hashlib.sha1()
		my_peer_id.update(str(os.getpid()).encode())
		my_peer_id.update(str(datetime.now()).encode())
		my_peer_id = my_peer_id.digest()
		self.torrent.peer_id = my_peer_id
		self.log_file.write("Peer_id" + str(my_peer_id) + "\n")
		self.log_file.write("info_hash:" + str(self.torrent.info_hash) + "\n")
		port = 6881
		message = b''.join([
            struct.pack('!Q', connection_id ),
            struct.pack('!I',1),
            struct.pack('!I', 123456),
            struct.pack('!20s',self.torrent.info_hash.digest()),
            my_peer_id,
            struct.pack('!Q', 0),
            struct.pack('!Q', self.torrent.length), #torrent_length
            struct.pack('!Q', 0),   #downloaded
            struct.pack('!I', 2),	#event(2:started)
            struct.pack('!I', 0),	#Default_ip
            struct.pack('!L', randint(0, 2**32)),	#key which has to be random
            struct.pack('!i', -1),               	#num_of_peers_we_want(-1 is default)
            struct.pack('!H',port)
        ])
		return self.send_msg(message)



	def send_msg(self,message):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		url = urlparse(self.trackers)
		hostname = url.hostname
		port = url.port
		address = (hostname,port)
		sock.sendto(message,address)

		try:
			response = sock.recv(1024)
			self.log_file.write("message sent and received successfully" + "\n")
			self.log_file.write("response : " + str(response) + "\n")
			return response
		except:
			self.log_file.write("Unable to connect to tracker")	

