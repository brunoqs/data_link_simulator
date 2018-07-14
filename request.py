'''
TODO: Estruturar o quadro a ser enviado de acordo com a especificacao do trabalho
      Dar um jeito de criar uma falha na mensagem



from socket import *
import random

# polinomio crc
polynomial_bitstring = "10100000000000011"

def crc_remainder(input_bitstring, polynomial_bitstring, initial_filler):
    len_input = len(input_bitstring)
    initial_padding = initial_filler * (len(polynomial_bitstring) - 1)
    input_padded_array = list(input_bitstring + initial_padding)
    polynomial_bitstring = polynomial_bitstring.lstrip('0')
    while '1' in input_padded_array[:len_input]:
        cur_shift = input_padded_array.index('1')
        for i in range(len(polynomial_bitstring)):
            if polynomial_bitstring[i] == input_padded_array[cur_shift + i]:
                input_padded_array[cur_shift + i] = '0'
            else:
                input_padded_array[cur_shift + i] = '1'
    return ''.join(input_padded_array)[len_input:]

# dados do servidor 
server_name = "127.0.0.1"
server_port = 12000

# criando conexao socket client - servidor
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

# flag de reenvio de pacote
resend = True

while resend:
    # enviando a mensagem e o crc gerado 
    crc_message = "0000000001000001" + crc_remainder("0000000001000001", polynomial_bitstring, "0")

    # randomizando um erro na mensagem que sera enviada
    if random.randrange(2) == 1:
        crc_message = crc_message[::-1]

    client_socket.send(crc_message.encode())

    # esperando confirmacao ou falha do servidor
    response = client_socket.recv(1024)

    # checando response do servidor ack ou nack
    if response == "ACK".encode():
        print("mensagem recebida pelo servidor com sucesso")
        resend = False
    else:
        print("mensagem corrompida, enviar novamente")
        resend = True

client_socket.close()'''

from link_layer import data_link
from ipaddress import IPv4Address

data_link.Data_Request(IPv4Address("127.0.0.1"), "teste")