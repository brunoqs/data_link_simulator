from link_layer import data_link
from ipaddress import IPv4Address

l_sdu = data_link.Data_Request(IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1"))
print('RECEIVED:', l_sdu)