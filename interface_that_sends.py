from ipaddress import IPv4Address
import csv
from link_layer.data_link import data_link

def manegement_module():
    with open('indication_log.csv') as csvfile:
        for reader in csv.reader(csvfile):
            print(reader, "\n")

source_address = str(input())
destination_address = str(input())
l_sdu = str(input())
#enviando um dado
data_link.Data_Indication(IPv4Address(destination_address), IPv4Address(source_address), l_sdu)
manegement_module()
