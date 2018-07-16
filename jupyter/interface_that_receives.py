from ipaddress import IPv4Address
import csv
from link_layer.data_link import data_link

def manegement_module():
    with open('request_log.csv') as csvfile:
        for reader in csv.reader(csvfile):
            print(reader, "\n")

data = data_link()
source_address = str(input())
destination_address = str(input())
data.Data_Request(IPv4Address(destination_address), IPv4Address(source_address))
#~ data.Data_Request(ipaddress.ip_address(destination_address), ipaddress.ip_address(source_address))
manegement_module()
