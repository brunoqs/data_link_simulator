import ipaddress
import csv
from link_layer.data_link import data_link

def manegement_module():
    with open('request_log.csv') as csvfile:
        for reader in csv.reader(csvfile):
            print(reader, "\n")

data = data_link()
destination_address = str(input())
l_sdu = str(input())
data.Data_Request(ipaddress.ip_address(destination_address), l_sdu)
manegement_module()
