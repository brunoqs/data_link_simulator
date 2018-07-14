import ipaddress
from link_layer.data_link import data_link

data = data_link()
destination_adress = str(input())
l_sdu = Data_Request(ipadress.ip_address(destination_address))

print("Message:", l_sdu)



#Montar as estatisticas com base nos dados do arquivo
logFile = open('logFile.txt', 'r')
result = logFile.readLines()
result = [s.rstrip() for s in result]#tirando os fins de linha e os espaços de cada posição da lista
result = [_str.split(' ') for _str in result]


 
