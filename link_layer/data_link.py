from .data_frame import data_frame
from .ack_frame import ack_frame

from physical_layer import physical_link

from ipaddress import IPv4Address 

class data_link:
	@staticmethod
	def Data_Request(destination_address, l_sdu):
		if type(destination_address) != IPv4Address:
			raise TypeError('destination_address must be IPv4Address.')
		if type(l_sdu) != int:
			raise TypeError('l_sdu must be int.')

		frame = data_frame(1, destination_address, IPv4Address("0.0.0.0"), "oioi")
		physical = physical_link(bin(frame.get_frame()))
		physical.F_Data_Request("ala")	

	@staticmethod
	def Data_Indication(destination_address, source_address, l_sdu):
		if type(destination_address) != IPv4Address:
			raise TypeError('destination_address must be IPv4Address.')
		if type(source_address) != IPv4Address:
			raise TypeError('source_address must be IPv4Address.')
		if type(l_sdu) != int:
			raise TypeError('l_sdu must be int.')

		ack = ack_frame(0, destination_address, source_address)
		physical = physical_link(bin(ack.get_frame()))
		physical.F_Data_Indication("ala")