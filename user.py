import ipaddress
from link_layer.data_frame import data_frame
from link_layer.data_link import data_link

data = data_link()#Construtor a ver
source_adress = str(input())
destination_address = str(input())

l_sdu = ''
data.Data_Request(ipadress.ip_address(destination_address))


l_sdu = data.Data_Indication(ipadress.ip_address(destination_address), #recebimento de dados
                         ipadress.ip_address(source_adress))

logFile = open('logFile.txt', 'r')
result = logFile.readLines() #Lendo o arquivo(log de erros)

result = [s.rstrip() for s in result]#tirando os fins de linha e os espaços de cada posição da lista
result = [_str.split(' ') for _str in result] 


def show_received_data(): #Os dados a serem mostrados aqui, são somente os retornados pela função?
    print(l_sdu)
    

def manegement_module(): #Módulo onde serão feitas as estatísticas com base no log de erros, sendo elas: mensagens enviadas \
                         #mensagens recebidas corretamente, erros detectados e retransmissões
    pass
