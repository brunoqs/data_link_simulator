from .data_frame import *
from .ack_frame import *

from physical_layer import physical_link

from ipaddress import IPv4Address

class data_link:
	@staticmethod
	def Data_Request(self, destination_address, l_sdu):
		frame = data_frame(1, destination_address, IPv4Address("0.0.0.0"), l_sdu)
		physical = physical_link(destination_address)
		frame_bitstring = bin(frame.get_frame()).lstrip("0b")
		
		lenght_bin = len(frame_bitstring)
		for i in range(0, lenght_bin, 8):
			physical.F_Data_Request(frame_bitstring[i:i+8])
	
		physical.fin_data()

		physical.close()

	@staticmethod
	def Data_Indication(self, destination_address, source_address):
		ack = ack_frame(0, destination_address, source_address)
		physical = physical_link(destination_address, source_address)
		
		while flag:
			request = physical.F_Data_Indication()
