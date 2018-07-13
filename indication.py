'''
TODO: Estruturar o quadro a ser enviado de acordo com a especificacao do trabalho
      Dar um jeito de criar uma falha na mensagem
'''
'''
from socket import *

# polinomio crc
polynomial_bitstring = "10100000000000011"

def crc_check(input_bitstring, polynomial_bitstring, check_value):

    len_input = len(input_bitstring)
    initial_padding = check_value
    input_padded_array = list(input_bitstring + initial_padding)
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            if polynomial_bitstring[i] == input_padded_array[cur_shift + i]:
                input_padded_array[cur_shift + i] = '0'
            else:
                input_padded_array[cur_shift + i] = '1'
    if '1' not in ''.join(input_padded_array)[len_input:]:
        return True
    else:
        return False 

# dados do servidor
server_name = "127.0.0.1"
server_port = 12000

# criando socket do servidor e setando suas config
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((server_name, server_port))
server_socket.listen(1)

# esperando client conectar para criar socket de conexao
connection_socket = server_socket.accept()[0]

# flag que aguarda um novo pacote, se o que chegou estiver errado
response = False

# Problema: se agente forçar o erro no pacote, ele entrará em loop
while not response:
    # recebendo dados do client
    request = connection_socket.recv(1024)

    # separando crc da mensagem e verificando a consistencia da mensagem
    crc = request[16:].decode("utf-8")
    message = request[:16].decode("utf-8")
    response = crc_check(message, polynomial_bitstring, crc)

    # enviando ack ou nack para client
    if response:
        connection_socket.send("ACK".encode())
    else:
        connection_socket.send("NACK".encode())

connection_socket.close() 
'''

from link_layer import data_link
from ipaddress import IPv4Address

data_link.Data_Indication(IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1"))