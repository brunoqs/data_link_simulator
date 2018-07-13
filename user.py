import ipaddress
from link_layer.data_frame import data_frame
from link_layer.data_link import data_link

data = data_link()#Construtor a ver
source_adress = str(input())
destination_address = str(input())

l_sdu = ''
try:
    l_sdu = data.Data_Request(ipadress.ip_address(destination_address))
except data_link as TimeOutError:#Erro na requisição de dados. Precisa contabilizar
    #contabilizar
except data_link as CRCError:
    #contabilizar
    
    

try: 
    l_sdu = data.Data_Indication(ipadress.ip_address(destination_address),
                         ipadress.ip_address(source_adress))
except data_link as TimeOutError: #Erro. Precisa contabilizar
    #contabilizar
except data_link as CRCError:
    #contabilizar


