from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from ipaddress import IPv4Address

import random
import time

from link_layer import data_frame
from link_layer import ack_frame

class physical_link:
	def __init__(self, destination_addr, source_addr=None, port=None):
		if type(destination_addr) != IPv4Address:
			raise TypeError('destination_addr must be IPv4Address.')
		if type(source_addr) != IPv4Address:
			raise TypeError('source_addr must be IPv4Address.')
		
		self.__dst = destination_addr
		self.__src = source_addr
		self.__port = port
		self.__socket = socket(AF_INET, SOCK_STREAM)

		# entra quando o Data_Request e chamado
		if source_addr != IPv4Address('0.0.0.0'):
			self.__socket.bind((str(self.__src), self.__port))
			self.__socket.listen(1)
			self.__connection_socket = self.__socket.accept()[0]
		else:
			# entra quando o Data_Indication e chamado
			self.__socket.connect((str(self.__dst), self.__port))


	def F_Data_Request(self, octeto):
		self.__socket.send(octeto.encode())
		time.sleep(0.01)

	def F_Data_Indication(self):
		recv = self.__connection_socket.recv(8)

		return recv
	
	def close(self):
		self.__socket.close()

	def fin_data(self):
		self.__socket.send("".encode())