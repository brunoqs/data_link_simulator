import ipaddress
import csv
from link_layer.data_link import data_link

def manegement_module():
    with open('indication_log.csv') as csvfile:
        for reader in csv.reader(csvfile):
            print(reader, "\n")

data = data_link()
source_address = str(input())
destination_address = str(input())
data.Data_Indication(ipaddress.ip_address(destination_address), #envia dado
                     ipaddress.ip_address(source_address))
manegement_module()
