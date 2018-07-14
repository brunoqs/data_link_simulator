from link_layer import data_link
from ipaddress import IPv4Address

l_sdu = input('SENDING: ')
data_link.Data_Indication(IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1"), l_sdu)

