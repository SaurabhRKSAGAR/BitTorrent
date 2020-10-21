import struct
class client:
		
	def __init__(self,arg1,arg2):
		self.info_hash = arg1
		self.peer_id = arg2


	def handshake_request(self):
		pstr = b'BitTorrent protocol'
		pstrlen = struct.pack("!B",len(pstr))
		reserved = struct.pack("!Q",0)
		z = self.info_hash.digest()
		x = self.convert_into_bytes(self.info_hash.digest())
		y = self.convert_into_bytes(self.peer_id)	


		handshake = pstrlen + pstr + reserved + x + y
		return handshake
								
	def interested_request(self):
		s = struct.pack("!I",1) + struct.pack("!B",2)
		return s
	

	def convert_into_bytes(self,string):
		result = b''
		for i in string:
			result = result + struct.pack("!B",i)
		return result	