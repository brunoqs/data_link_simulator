from link_layer import data_link
from ipaddress import IPv4Address

# PC roda request.py
# l_sdu = data_link.Data_Request(IPv4Address("192.168.0.107"), IPv4Address("192.168.0.100"))

# localhost <--> localhost
l_sdu = data_link.Data_Request(IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1"))

print('RECEIVED:', l_sdu)

