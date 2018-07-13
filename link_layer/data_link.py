from .data_frame import *
from .ack_frame import *

from physical_layer import physical_link

from ipaddress import IPv4Address

import time

class data_link:
	@staticmethod
	def Data_Request(destination_address, l_sdu):
		frame = data_frame(1, destination_address, IPv4Address("0.0.0.0"), l_sdu)
		
		reesend = True
		while reesend: # enquanto receber nack
			# envia um frame
			physical_send = physical_link(destination_address, IPv4Address("0.0.0.0"), 11000)
			frame_bitstring = bin(frame.get_frame()).lstrip("0b")
			lenght_bin = len(frame_bitstring)
			for i in range(0, lenght_bin, 8):
				physical_send.F_Data_Request(frame_bitstring[i:i+8])
			physical_send.close()

			# espera 1s para ficar esperando um ack ou nack
			time.sleep(1)
			physical_recv = physical_link(destination_address, IPv4Address("127.0.0.1"), 12000)
			ack = ""
			flag = True
			while flag:
				request = physical_recv.F_Data_Indication()
				print(request.decode())
				if request:
					ack += request.decode()
				else:
					flag = False
			print (ack)
			# abre um ack para ver seu sequence 0=ack 1=nack
			ack_check = ack_frame(bin_flow_recv=int(ack, base=2))
			n_ack = bin(ack_check.get_sequence()).lstrip("0b")
			if n_ack == "1":
				reesend = True
			else:
				reesend = False
			physical_recv.close()

	@staticmethod
	def Data_Indication(destination_address, source_address):
		ack = ack_frame(0, destination_address, source_address)
		
		response = True
		while response: # enquanto tiver que esperar outro pacote
			# espera o frame
			physical_recv = physical_link(destination_address, source_address, 11000)
			frame = ""
			flag = True
			while flag:
				request = physical_recv.F_Data_Indication()
				print(request.decode())
				if request:
					frame += request.decode()
				else:
					flag = False
			print (frame)
			physical_recv.close()

			# espera 2s para enviar um ack apos abrir o frame e testar o crc
			time.sleep(2)
			physical_send = physical_link(destination_address, IPv4Address("0.0.0.0"), 12000)
			frame_check = data_frame(bin_flow_recv=int(frame, base=2))
			# crc = True envia ack com sequence = 0 (ack)
			if frame_check.crc_check():
				ack_bitstring = bin(ack.get_frame()).lstrip("0b")
				lenght_bin = len(ack_bitstring)
				for i in range(0, lenght_bin, 8):
					physical_send.F_Data_Request(ack_bitstring[i:i+8])
				physical_send.close()

				response = False # nao precisa esperar outro frame
			# crc = False envia ack com sequence = 1 (nack)
			else:
				ack.set_sequence(0b00000001) #nack
				ack_bitstring = bin(ack.get_frame()).lstrip("0b")
				lenght_bin = len(ack_bitstring)
				for i in range(0, lenght_bin, 8):
					physical_send.F_Data_Request(ack_bitstring[i:i+8])
				physical_send.close()

				response = True # precisa esperar outro frame