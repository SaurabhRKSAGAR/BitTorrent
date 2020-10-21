import struct
import requests
import bencode
import hashlib
import socket
from urllib.parse import urlparse, urlencode
import os
from datetime import datetime
import time
from random import randint
class http_connection():
	def __init__(self, torrent,tracker_list):
		self.tracker = tracker_list
		self.t = torrent
		self.log_file = open(torrent.log_file_name + ".txt","a")

	def get_parameters(self):
		version_number = 100
		my_peer_id = hashlib.sha1()
		my_peer_id.update(str(os.getpid()).encode())
		my_peer_id.update(str(datetime.now()).encode())
		my_peer_id = my_peer_id.digest()
		self.t.peer_id = my_peer_id
		self.log_file.write("HTTP Connection \n")
		#print(my_peer_id)
		self.log_file.write("peer-id:" + str(my_peer_id) + "\n")
 
		parameters = {'info_hash': self.t.info_hash.digest(),
					  'peer_id': my_peer_id,
					  'port':3128,
					  'left':self.t.length,
					  'compact':1,
					  'event':'started',
					  'uploaded':0,
					  'downloaded':0
					  }
		return parameters


	def connect_to_tracker(self):
		#print(self.tracker)
		x = self.get_parameters()
		response = requests.get(self.tracker,params = x)
		#print(response.request.url)
		self.log_file.write("Tracker response received successfully" + "\n")
		#print(response.content)
		self.log_file.write("response :" + str(response.content))

		if(response.status_code == 200):
			#print("TRUE")
			#print(bencode.bdecode(response.content))
			data_extracted_from_tracker = bencode.decode(response.content)
			#print("PEER LIST")
			self.log_file.write("Peer List:" + str(data_extracted_from_tracker['peers']))
			#print(data_extracted_from_tracker['peers'])
			self.log_file.close()
			return data_extracted_from_tracker
			#response_data_from_tracker = bencode.bdecode(response.content)
		else:
			print("Unable to connect_to_tracker")	
			return 