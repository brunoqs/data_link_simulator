from .data_frame import data_frame
from .ack_frame import ack_frame

from physical_layer import physical_link

from ipaddress import IPv4Address 

import time

class data_link:
	@staticmethod
	def Data_Indication(destination_address, source_address, l_sdu):
		frame = data_frame(1, destination_address, IPv4Address("0.0.0.0"), l_sdu)
		port_serv = 11000
		port_client = 12000

		resend = True
		while resend: # enquanto receber nack
			# envia um frame
			physical_send = physical_link(destination_address, IPv4Address("0.0.0.0"), port_serv)
			frame_bitstring = bin(frame.get_frame()).lstrip("0b")
			lenght_bin = len(frame_bitstring)
			for i in range(0, lenght_bin, 8):
				physical_send.F_Data_Indication(frame_bitstring[i:i+8])
			physical_send.close()

			# espera 1s para ficar esperando um ack ou nack
			time.sleep(1)
			physical_recv = physical_link(destination_address, source_address, port_client)
			ack = ""
			flag = True
			while flag:
				request = physical_recv.F_Data_Request()
				if request:
					ack += request.decode()
				else:
					flag = False

			# abre um ack para ver seu sequence 0=ack 1=nack
			ack_check = ack_frame(bin_flow_recv=int(ack, base=2)) 
			n_ack = ack_check.get_sequence()
			if n_ack == 0b00000001:
				resend = True
			else:
				resend = False
			physical_recv.close()

			port_client += 1
			port_serv += 1

	@staticmethod
	def Data_Request(destination_address, source_address):
		ack = ack_frame(0, destination_address, source_address)
		port_serv = 12000
		port_client = 11000

		response = True
		while response: # enquanto tiver que esperar outro pacote
			# espera o frame
			physical_recv = physical_link(destination_address, source_address, port_client)
			frame = ""
			flag = True
			while flag:
				request = physical_recv.F_Data_Request()
				if request:
					frame += request.decode()
				else:
					flag = False

			physical_recv.close()

			# espera 2s para enviar um ack apos abrir o frame e testar o crc
			time.sleep(2)
			physical_send = physical_link(destination_address, IPv4Address("0.0.0.0"), port_serv)
			frame_check = data_frame(bin_flow_recv=int(frame, base=2))
			# crc = True envia ack com sequence = 0 (ack)
			if frame_check.crc_check():
				ack_bitstring = bin(ack.get_frame()).lstrip("0b")
				lenght_bin = len(ack_bitstring)
				for i in range(0, lenght_bin, 8):
					physical_send.F_Data_Indication(ack_bitstring[i:i+8], True)
				physical_send.close()

				response = False # nao precisa esperar outro frame
			# crc = False envia ack com sequence = 1 (nack)
			else:
				ack.set_sequence(1) #nack
				ack_bitstring = bin(ack.get_frame()).lstrip("0b")
				lenght_bin = len(ack_bitstring)
				for i in range(0, lenght_bin, 8):
					physical_send.F_Data_Indication(ack_bitstring[i:i+8], True)
				physical_send.close()

				response = True # precisa esperar outro frame

			ack.set_sequence(0) # apos enviar um nack voltar para ack
			port_client += 1
			port_serv += 1
		
		return data_frame.bin_to_str(frame_check.get_payload()) # l_sdu
