import bencode
import socket
import requests
import hashlib
import sys
import random
from random import randint
import os
from datetime import datetime
import struct
import threading
from urllib.parse import urlparse, urlencode
import bitarray
import time
from client import *
from decode_torrent import *
from udp_conn import *
from http_conn import *
from peer_ip_extraction import *
from peer_connection import *

class chk_existance(object):
	def __init__(self):
		self.torrent_file = ""
		self.path = ""

	def chk_torrent_file(self,torrent_file):
		self.torrent_file = torrent_file
		while(not os.path.isfile(self.torrent_file)):
			print("File not found")
			print("------------------------------------------------")
			self.torrent_file = input("Enter torrent file name again \n")
		print("---------------------------")	
		return self.torrent_file	

	def chk_path(self,path):
		self.path = path
		while(not os.path.exists(self.path)):
			print("Path not found")
			print("------------------------------------------------")
			self.path = input("Enter Path \n")
		print("---------------------------")
		return self.path		



				

if __name__ == "__main__":
	check_path_and_locations = chk_existance() 
	torrent_name = input("Enter torrent file name \n")
	torrent_file = check_path_and_locations.chk_torrent_file(torrent_name)
	path = input("Enter the location where you want to store the file \n")
	location = check_path_and_locations.chk_path(path)
	file_name = input("Enter the file name \n")	
	print("-----------------------------")
	log_file = input("Please enter the name for log_file \n")
	print("-----------------------------")
	file_location = os.path.join(location,file_name + ".bin")
	t = decode_torrent(torrent_file,file_location,log_file)
	tracker_url = urlparse(t.announce)
	if(tracker_url.scheme == "udp"):
		conn = udp_conn(t,t.announce)
		peer_ip = conn.connection_udp()
		scheme = 'udp'
	else:
		conn = http_connection(t,t.announce)
		peer_ip = conn.connect_to_tracker()	
		scheme = 'http'
	print("Connection with torrent successful")
	peers = peer_ip_extraction(peer_ip,scheme,t)
	peer_ips = peers.ip_extraction()
	peer_conn = peer_connection(peer_ips,t)
	torrent_client = client(t.info_hash,t.peer_id)
	handshake = torrent_client.handshake_request()
	intersted_msg = torrent_client.interested_request()
	print("Peer List extracted successfully")
	t_main = threading.Thread(target=peer_conn.connection_of_peer_with_client, args = (handshake,intersted_msg)) 
	t_main.start()	




		



