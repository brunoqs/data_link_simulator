import ipaddress
from link_layer.data_link import data_link

data = data_link()#Construtor a ver
source_address = str(input())
destination_address = str(input())
data.Data_Indication(ipaddress.ip_address(destination_address), #envia dado
                     ipaddress.ip_address(source_address))
    




    
