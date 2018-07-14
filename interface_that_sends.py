import ipaddress
from link_layer.data_link import data_link

data = data_link()#Construtor a ver
source_adress = str(input())
destination_address = str(input())
data.Data_Indication(ipadress.ip_address(destination_address), #envia dado
                     ipadress.ip_address(source_adress))
    




    
