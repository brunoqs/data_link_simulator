from link_layer import data_link
from ipaddress import IPv4Address

l_sdu = input('SENDING: ')
data_link.Data_Indication(IPv4Address("192.168.0.100"), IPv4Address("192.168.0.107"), l_sdu)

# VM roda indication.py