from ipaddress import IPv4Address
import csv
from link_layer.data_link import data_link

def manegement_module():
    with open('indication_log.csv') as csvfile:
        for reader in csv.reader(csvfile):
            print(reader, "\n")

# No trecho a seguir é recebido um ip fonte e um destino
# e um dado 'l_sdu' que será enviado do ip fonte para o ip
# destino.
source_address = str(input())
destination_address = str(input())
l_sdu = str(input())
# Enviando o dado.
data_link.Data_Indication(IPv4Address(destination_address), 
                            IPv4Address(source_address), l_sdu)
# Módulo de gerenciamento em que gera as informações dos dados
# enviados.
manegement_module()
