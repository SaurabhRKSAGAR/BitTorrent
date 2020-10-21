from download_start import *
class rare_piece_extraction(object):

	def __init__(self,sock,bitfield,t,i):
		self.sock = sock
		self.bitfield = bitfield
		self.torrent = t
		self.piece_num = i

	def execute_process_in_thread(self):
		download_piece = download_start(self.sock,self.bitfield,self.torrent)
		piece_data = download_piece.get_piece(self.piece_num,self.torrent.block_length,self.torrent.last_block_size)
		download_piece.update_bitfield(self.piece_num)
		download_piece.write_into_file(self.piece_num,piece_data)	
