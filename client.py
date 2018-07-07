'''
TODO: Reenviar os dados quando receber um NACK
      Estruturar o quadro a ser enviado de acordo com a especificacao do trabalho
      Dar um jeito de criar uma falha na mensagem

'''

from socket import *

# polinomio crc
polynomial_bitstring = "10100000000000011"

def crc_remainder(input_bitstring, polynomial_bitstring, initial_filler):
    '''
    Calculates the CRC remainder of a string of bits using a chosen polynomial.
    initial_filler should be '1' or '0'.
    '''
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

# enviando a mensagem e o crc gerado 
crc_message = "0000000001000001" + crc_remainder("0000000001000001", polynomial_bitstring, "0")
client_socket.send(crc_message.encode())

# esperando confirmacao ou falha do servidor
response = client_socket.recv(1024)

# checando response do servidor ack ou nack(todo)
if response == "ACK".encode():
    print("mensagem recebida pelo servidor com sucesso")
else:
    print("mensagem corrompida, enviar novamente")

client_socket.close()