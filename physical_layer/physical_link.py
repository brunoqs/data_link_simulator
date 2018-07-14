from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from ipaddress import IPv4Address
from random import randint

import time

from link_layer import data_frame
from link_layer import ack_frame

class physical_link:
    def __init__(self, destination_addr, source_addr=IPv4Address('0.0.0.0'), port=0):
        if type(destination_addr) != IPv4Address:
            raise TypeError('destination_addr must be IPv4Address.')
        if type(source_addr) != IPv4Address:
            raise TypeError('source_addr must be IPv4Address.')
        if type(port) != int:
            raise TypeError('port must be int.')
        
        self.__dst = destination_addr
        self.__src = source_addr
        self.__port = port
        self.__socket = socket(AF_INET, SOCK_STREAM)

        # entra quando o Data_Indication e chamado
        if source_addr != IPv4Address('0.0.0.0'):
            self.__socket.bind((str(self.__src), self.__port))
            self.__socket.listen(1)
            self.__connection_socket = self.__socket.accept()[0]
        else:
            # entra quando o Data_Request e chamado
            self.__socket.connect((str(self.__dst), self.__port))

    def F_Data_Indication(self, octeto, ack=None):
        if ack == None:
            if self.__random_noisy_tx():
                octeto = self.__damage_packet(octeto)
        self.__socket.send(octeto.encode())
        time.sleep(0.01)

    def F_Data_Request(self):
        return self.__connection_socket.recv(8)
    
    def close(self):
        self.__socket.close()
    
    def __random_packet_loss(self):
        return randint(0, 1000) == randint(400, 600)
    
    def __random_noisy_tx(self):
        return randint(0, 100) == randint(40, 60)
    
    def __damage_packet(self, octeto):
        binary = int(octeto, base=2)
        binary ^= 0b10101010
        binary |= 0b10000000
        return bin(binary).lstrip('0b')