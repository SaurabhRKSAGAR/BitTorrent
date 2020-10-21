import bencode
import hashlib
import sys
class decode_torrent:

	def __init__(self,file_name,path,log_file):
		f = open(file_name,"rb")
		self.log_file_name = log_file
		self.log_file = open(self.log_file_name + ".txt","w+")
		data = bencode.bdecode(f.read())
		self.announce = data['announce']
		self.log_file.write("Tracker:" + str(self.announce) + "\n")

		self.download_path = path

		self.List = data['announce-list']
		self.log_file.write("announce-list:\n")
		for strct in self.List:
			self.log_file.write(str(strct)+ "\n")

			
		self.piece_length = data['info']['piece length']
		self.log_file.write("piece_length:" + str(self.piece_length) + "\n")

		self.name = data['info']['name']
		self.log_file.write(str(self.name))

		n = data['info']['pieces']
		assert len(n) % 20 == 0
		self.no_of_pieces = len(n)/20
		self.log_file.write(str(self.no_of_pieces) + "\n")

		self.info_hash = hashlib.sha1(bencode.encode(data['info']))
		self.log_file.write("info-hash:"+ str(self.info_hash) + "\n")

		try:
			self.length = data['info']['length']
		except KeyError:
			self.length = sum(eachfile['length'] for eachfile in data['info']['files'])

		self.log_file.write("length:" + str(self.length) + "\n")
		self.peer_id = ""	
		self.block_length = min(2**14, self.piece_length)
		self.log_file.write("block_length:"+ str(self.block_length) + "\n")
		self.whole_blocks_per_piece = self.piece_length / self.block_length

		self.log_file.write("No.of blocks per piece:"+ str(self.whole_blocks_per_piece) + "\n")
		self.last_block_size = self.piece_length % self.block_length

		self.log_file.write("last_block_size:"+ str(self.last_block_size) + "\n")
		self.log_file.write("---------------------------------------------------------")
		self.log_file.close()
		print("Torrent decode successfull")

