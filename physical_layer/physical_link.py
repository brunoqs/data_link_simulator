from socket import *
import random

class physical_link:
	def __init__(self, bin):
		self.bin = bin
	
	def F_Data_Request(self, octeto):
		server_name = "127.0.0.1"
		server_port = 12000

		client_socket = socket(AF_INET, SOCK_STREAM)
		client_socket.connect((server_name, server_port))
		
		lenght_bin = len(self.bin) 
		for i in range(0,lenght_bin, 4):
			client_socket.send(self.bin[i:i+4].encode())

		client_socket.close()

	def F_Data_Indication(self, octeto):
		server_name = "127.0.0.1"
		server_port = 12000

		server_socket = socket(AF_INET, SOCK_STREAM)
		server_socket.bind((server_name, server_port))
		server_socket.listen(1)    

		connection_socket = server_socket.accept()[0]

		frame = ""
		while len(frame) != len(self.bin):
			request = connection_socket.recv(1024)
			frame += request.decode("utf-8")

		print(frame)

		connection_socket.close()