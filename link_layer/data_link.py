from link_layer import data_frame
from link_layer import ack_frame

from physical_layer import physical_link

from ipaddress import IPv4Address

class data_link():
    def __init__(self):
        self.frame = data_frame.data_frame(1, IPv4Address("127.0.0.1"), IPv4Address("0.0.0.0"), "oioi")
        self.physical = physical_link.physical_link(bin(self.frame.get_frame()))
    
    def Data_Request(self, destination_address, l_sdu):
    	self.physical.F_Data_Request("ala")	

    def Data_Indication(self, destination_address, source_address, l_sdu):
    	self.physical.F_Data_Indication("ala")	
