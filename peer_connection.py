import threading
from rare_piece_extraction import *
import socket
from download_start import *
from bitstring import BitArray
class peer_connection:
	def __init__(self, ips,t):
		self.peer_connection_ips = ips
		self.connected_peers = []
		self.bitfield = b''
		self.torrent = t
		self.log_file = open(t.log_file_name + ".txt" , "a")
		self.sock = ""

	def thread_creation_for_rarest_first(self,ip,port,handshake,intersted_msg):
		t1 = threading.Thread(target=self.rarest_first, args = (ip,port,handshake,intersted_msg)) 
		t1.start()	
	

	def socket_connection(self,ip,port,handshake,intersted_msg,download):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.log_file.write(str(ip))
			sock.connect((ip, port))
			self.Peer_Connection_with_requests(handshake,intersted_msg,sock,download)		
		except:
			print("Cannot connect to :" , ip , port)
			
		
	
	def connection_of_peer_with_client(self,handshake,intersted_msg):
		print("Connecting with peers...")
		download = download_start(self.torrent)
		for ip , port in self.peer_connection_ips:
			if(self.socket_connection(ip,port,handshake,intersted_msg,download)):
				print("TRUE")

	
	def single_connection(self,handshake,intersted_msg):
		ip,port = self.peer_connection_ips[0]
		self.socket_connection(ip,port,handshake,intersted_msg)

				

	def send_handshake(self,handshake,sock):
		sock.send(handshake)
		received_handshake_msg = sock.recv(68)


	def send_interested_msg(self,intersted_msg,sock):
		sock.send(intersted_msg)
		received_interested_msg_length = sock.recv(4)
		received_interested_msg_id = sock.recv(1)
		interested_id = struct.unpack("!B",received_interested_msg_id)
		return interested_id[0]

	def Peer_Connection_with_requests(self,handshake,intersted_msg,sock,download):	
		self.send_handshake(handshake,sock)
		received_bitfield_length = sock.recv(4)                  # Gives length of bitfield msg
		received_id = sock.recv(1)						  	     #Gives id of bitfield msg i.e.(5)
		x = struct.unpack("!I",received_bitfield_length)
		received_bitfield = sock.recv(x[0])                      #Unpack returns a tuple thats why x[0]											  #for finding remaining pieces if any
		self.bitfield = received_bitfield
		new_bitfield = BitArray(bytes = received_bitfield)
		# print(new_bitfield.bin)
		# print(len(new_bitfield))
		# print(type(received_bitfield))
		#print("bitfield:" ,received_bitfield)
		self.log_file.write("Recived bitfield:" + str(received_bitfield) + "\n")
		interested_id = self.send_interested_msg(intersted_msg,sock)

		if(interested_id == 1):
			
			self.log_file.write("Client Unchoked \n")
			#download = download_start(sock,new_bitfield,self.torrent)
			print("STATRTING DOWNLOAD... \n")
			print("---------------------------")
			self.log_file.write("download started \n")
			self.log_file.close()
			t2 = threading.Thread(target=self.check_remaining_pieces, args = (new_bitfield,received_bitfield_length)) 
			t2.start()
			download.get_data_from_peers(sock,new_bitfield) 
		else:	
			self.log_file.write("Client is Choked \n")

	def connecting_msg_to_peer(self,ip,port,handshake,intersted_msg):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((ip,port))		
			sock.send_handshake(handshake,sock)
			self.sock = sock
			print("SUCEESS in handshake in thread")
			interested_id = sock.send_interested_msg(intersted_msg,sock)
			if(interested_id == 1):
				print("Client Unchoked")
				return True
			else:
				print("Choked")	
				return False
		except:
			print("Unable to connect",ip,port)	
	
	def check_remaining_pieces(self,bitfield):
		bitarray_for_remaining_pieces = bitfield
		length_of_bitfield = len(bitarray_for_remaining_pieces)
		for i in length_of_bitfield:
			if(bitarray_for_remaining_pieces[i] == 0):
				for ip,port in self.peer_connection_ips:
					if(connecting_msg_to_peer(ip,port,handshake,intersted_msg)):
						r = rare_piece_extraction(self.sock,bitarray_for_remaining_pieces,self.torrent,i)
						t3 = threading.Thread(target=r.execute_process_in_thread, args = ()) 
						t3.start()	

