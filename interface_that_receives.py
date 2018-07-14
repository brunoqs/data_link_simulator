import ipaddress
from link_layer.data_link import data_link

data = data_link()
destination_address = str(input())
l_sdu = str(input())
data.Data_Request(ipaddress.ip_address(destination_address), l_sdu)




#Montar as estatisticas com base nos dados do arquivo
logFile = open('logFile.txt', 'r')
result = logFile.readLines()
result = [s.rstrip() for s in result]#tirando os fins de linha e os espaços de cada posição da lista
result = [_str.split(' ') for _str in result]


 
