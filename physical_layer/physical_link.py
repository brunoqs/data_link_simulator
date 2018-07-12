import random
import time

from link_layer import data_frame
from link_layer import ack_frame

from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM

class physical_link(data_frame, ack_frame):
	def __init__(self, bin):
		self.__bin = bin
		self.__frame_recv = ""
	
	def F_Data_Request(self, octeto):
		server_name = "127.0.0.1"
		server_port = 12000

		client_socket = socket(AF_INET, SOCK_STREAM)
		client_socket.connect((server_name, server_port))
		
		lenght_bin = len(self.__bin) 
		for i in range(0,lenght_bin, 4):
			client_socket.send(self.__bin[i:i+4].encode())
			time.sleep(0.01)
		client_socket.send("None".encode())

		print("before send: " + str(self.__bin))

		client_socket.close()

	def F_Data_Indication(self, octeto):
		server_name = "127.0.0.1"
		server_port = 12000

		server_socket = socket(AF_INET, SOCK_STREAM)
		server_socket.bind((server_name, server_port))
		server_socket.listen(1)    

		connection_socket = server_socket.accept()[0]

		frame = ""
		flag = True
		while flag:
			request = connection_socket.recv(1024)
			print(request)
			if request != "None".encode():
				frame += request.decode("utf-8")
			else:
				flag = False

		print("after send: " + str(frame))
		self.set_frame(self.str_to_bin(frame))
		print (self.crc_check())

		connection_socket.close()