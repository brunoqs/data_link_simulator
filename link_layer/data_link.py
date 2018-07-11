from data_frame import *
from ack_frame import *

import sys
sys.path.append('../physical_layer/')
from physical_link import *

from ipaddress import IPv4Address

class data_link:
    def __init__(self):
        self.frame = data_frame(1, IPv4Address("127.0.0.1"), IPv4Address("0.0.0.0"), "oioi")
        self.physical = physical_link(bin(self.frame.get_frame()))
    
    def Data_Request(self, destination_address, l_sdu):
    	self.physical.F_Data_Request("ala")	

    def Data_Indication(self, destination_address, source_address, l_sdu):
    	self.physical.F_Data_Indication("ala")	
