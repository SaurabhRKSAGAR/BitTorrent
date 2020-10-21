import struct
class peer_ip_extraction:
	def __init__(self,tracker_data,scheme,t):
		self.tracker_data_for_peers = tracker_data
		self.scheme = scheme
		self.log_file = open(t.log_file_name + ".txt" , "a")

	def ip_extraction(self):
		if(self.scheme == 'udp'):
			peer_list = self.tracker_data_for_peers
		else:	
			peer_list = self.tracker_data_for_peers['peers']
		
		peer_ip_addresses = []
		self.log_file.write("\n Peer List: \n")
		for i in range (0, len(peer_list), 6):
			ip = ()
			for c in peer_list[i:i+4]:
					ip += (c,)
			if(len(ip) < 4):
				continue		
			ip_string = "%s.%s.%s.%s" %(ip)
			port = struct.unpack('!H', peer_list[i+4:i+6])
			port = "%s" % (port)
			port = int(port)
			ip_and_port = (ip_string, port)
			self.log_file.write(str(ip_and_port) + "\n")
			peer_ip_addresses.append(ip_and_port)

		self.log_file.close()	
		return peer_ip_addresses