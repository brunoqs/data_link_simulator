import time
from ipaddress import IPv4Address
from random import randint
from socket import AF_INET, SOCK_STREAM, socket

from link_layer import ack_frame, data_frame

class physical_link:
    """Classe que simula a camada física da rede."""

    def __init__(self, destination_addr, source_addr=IPv4Address('0.0.0.0'), port=0):
        """Construtor.
        @param destination_addr : IPv4Address
        @param source_addr : IPv4Address (default IPv4Address('0.0.0.0'))
        @param port : int (default 0)"""

        # corretude dos parâmteros.
        if type(destination_addr) != IPv4Address:
            raise TypeError('destination_addr must be IPv4Address.')
        if type(source_addr) != IPv4Address:
            raise TypeError('source_addr must be IPv4Address.')
        if type(port) != int:
            raise TypeError('port must be int.')
        
        # atributos privados do objeto:
        self.__dst = destination_addr                # endereço de destino
        self.__src = source_addr                     # endereço de origem
        self.__port = port                           # porta do socket
        self.__socket = socket(AF_INET, SOCK_STREAM) # socket usado na comunicação

        if source_addr != IPv4Address('0.0.0.0'):
            # entra quando o Data_Indication é chamado.
            self.__socket.bind((str(self.__src), self.__port))
            self.__socket.listen(1)
            # cria o atributo privado para a conexão:
            self.__connection_socket = self.__socket.accept()[0]
        else:
            # entra quando o Data_Request é chamado.
            self.__socket.connect((str(self.__dst), self.__port))

    def F_Data_Indication(self, octeto, ack=None):
        """Método responsável por enviar um octeto pela camada física.
        @param octeto : str (composta somente por '1's e '0's)"""

        if ack == None:
            # de vez em quando, aleatoriamente gera erros nos bits.
             if self.__random_noisy_tx():
                 octeto = self.__damage_packet(octeto)
        self.__socket.send(octeto.encode()) # envia o octeto pelo socket.
        time.sleep(0.01) # delay para o outro socket poder sincronizar.

    def F_Data_Request(self):
        """Método que retorna um octeto recebido.
        @return bytes"""

        return self.__connection_socket.recv(8) # tamanho do buffer de 8 bytes (1 octeto).
    
    def close(self):
        """Método que fecha a conexão do socket para liberar os recursos."""
        self.__socket.close()
    
    def __random_packet_loss(self):
        """Método privado para auxiliar nas aleatoriedades."""
        return randint(0, 1000) == randint(400, 600)
    
    def __random_noisy_tx(self):
        """Método privado para auxiliar nas aleatoriedades."""
        return randint(0, 200) == randint(91, 99)
    
    def __damage_packet(self, octeto):
        """Método privado para simular danos nos bits."""
        binary = int(octeto, base=2)
        binary ^= 0b10101010
        binary |= 0b10000000
        return bin(binary).lstrip('0b')