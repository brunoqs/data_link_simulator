from .data_frame import *
from .ack_frame import *

from physical_layer import physical_link

from ipaddress import IPv4Address

class data_link():
	def __init__(self):
		pass

	def Data_Request(self, destination_address, l_sdu):
		self.frame = data_frame(1, IPv4Address("127.0.0.1"), IPv4Address("0.0.0.0"), "oioi")
		self.physical = physical_link(bin(self.frame.get_frame()))
		self.physical.F_Data_Request("ala")	

	def Data_Indication(self, destination_address, source_address, l_sdu):
		self.ack = ack_frame(0, IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1"))
		self.physical = physical_link(bin(self.ack.get_frame()))
		self.physical.F_Data_Indication("ala")	
