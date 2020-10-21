import bitarray
import struct
import sys
import time
from progress.bar import Bar
class download_start(object):
	def __init__(self,t):
		self.sock = ""
		self.torrent = t
		self.downloaded_file = open(t.download_path,'wb+')
		self.log_file = open(t.log_file_name + ".txt", "a")
		print("No.Of pieces : " , int(self.torrent.no_of_pieces))
		self.bitfield = ""
		self.bitarray_in_torrent = bitarray.bitarray(int(self.torrent.no_of_pieces))

	def init_bitarray_in_torrent(self):
		no_of_pieces = self.torrent.no_of_pieces 
		for i in range(int(no_of_pieces)):
			self.bitarray_in_torrent[i] = 0


	def create_request_msg(self,piece_num,offset,block_length):

		msg_length = struct.pack("!I",13)
		msg_id = struct.pack("!B",6)
		piece_index = struct.pack("!I",piece_num)
		piece_offset = struct.pack("!I",offset)
		piece_length = struct.pack("!I",block_length)
		request_msg = msg_length + msg_id + piece_index + piece_offset + piece_length 
		self.log_file.write("REQUEST msg created successfully and sending \n")
		self.send_request(request_msg,piece_num,offset,block_length)

	def send_request(self,request_msg,piece_num,offset,block_length):
		self.sock.send(request_msg)
		received_msg_after_request = self.sock.recv(4)
		received_id_after_request = self.sock.recv(1)
		received_id_after_request = struct.unpack("!B",received_id_after_request)
		if(received_id_after_request[0] == 7):
			self.log_file.write("REQUEST sent and piece id received \n")
		else:
			self.log_file.write("REQUEST failed and sending again \n")	
			self.create_request_msg(request_msg,piece_num,offset,block_length)
			

	def get_block(self,piece_num, block_num, block_length):
		block_data = b''
		self.create_request_msg(piece_num, block_num*block_length, block_length)
		piece_msg = self.sock.recv(8)
		while len(block_data) < (int(self.torrent.block_length)):
			time.sleep(1)
			block_data += self.sock.recv(2**14)
		#print("SUCEESS IN BLOCK RECEPTION")
		self.log_file.write("Block received successfully \n")	
		self.log_file.write("------------------------------------------------------------- \n")
		return block_data

	def get_data_from_peers(self,sock,new_bitfield):
		self.init_bitarray_in_torrent()
		self.bitfield = new_bitfield
		self.sock = sock
		for piece_num in range(len(self.bitarray_in_torrent)):
			self.log_file = open(self.torrent.log_file_name + ".txt","a") 
			if(self.bitfield[piece_num] and self.bitarray_in_torrent[piece_num] == 0):
				self.log_file.write("REQUEST SEND \n")
				piece_data = self.get_piece(piece_num,self.torrent.block_length,self.torrent.last_block_size)
				self.update_bitfield(piece_num)
				self.write_into_file(piece_num,piece_data)
				print(" \n Download Percentage: " , (piece_num+1)/self.torrent.no_of_pieces)
				self.log_file.close()
				

	def update_bitfield(self,index):
		self.bitarray_in_torrent[index] = 1

				
	def get_piece(self,piece_num,block_length,last_block_size):
		piece_data = b''
		if(self.bitfield[piece_num]):
			bar = Bar('Block Download:',max = int(self.torrent.whole_blocks_per_piece))
			for block_num in range(int(self.torrent.whole_blocks_per_piece)):
				#print(block_num)
				bar.next()
				self.log_file.write("Requesting block num:" + str(block_num) + "\n")
				block = self.get_block(piece_num, block_num, block_length)
				piece_data += block
			if last_block_size:
				block = self.get_block(piece_num, block_num, last_block_size)
				piece_data += block
			self.log_file.write("Piece received successfully :" + str(piece_num) + "\n")	
			return piece_data
	 
	def write_into_file(self,location,data):
		n = len(data)
		self.downloaded_file.seek(location*n)
		self.downloaded_file.write(data)
		self.log_file.write("Data written successfully \n")
