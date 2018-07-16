from ipaddress import IPv4Address
import csv
from link_layer.data_link import data_link

def manegement_module():
    with open('request_log.csv') as csvfile:
        for reader in csv.reader(csvfile):
            print(reader, "\n")

# No trecho a seguir é recebido um ip fonte e um ip destino
# em que será feito uma requisição do que foi passado do 
# origem para o destino.
source_address = str(input())
destination_address = str(input())
# Fazendo a requisição.
data_link.Data_Request(IPv4Address(destination_address), IPv4Address(source_address))
# Módulo de gerenciamento em que gera as informações dos dados
# recebidos.
manegement_module()
