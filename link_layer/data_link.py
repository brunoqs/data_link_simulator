from .data_frame import data_frame
from .ack_frame import ack_frame

from physical_layer import physical_link

from ipaddress import IPv4Address 

import time

class data_link:
	__SEQ_ONE = 0b00000000 # stop-and-wait
	__SEQ_TWO = 0b10000000 # stop-and-wait
	__SEQ_UNIQUE_FRAME = 0b00000001 # único quadro
	__SEQ_LAST_FRAME = 0b10000001 # indica o último quadro enviado
	__ACK_ONE = 0b00000001
	__ACK_TWO = 0b10000001
	__NACK_ONE = 0b00000000
	__NACK_TWO = 0b10000000

	@staticmethod
	def Data_Indication(destination_address, source_address, l_sdu):
		port_serv = 11000
		port_client = 12000

		payload_len = len(l_sdu.encode())

		if payload_len <= 255:
			frame = data_frame(data_link.__SEQ_UNIQUE_FRAME, destination_address, IPv4Address("0.0.0.0"), l_sdu)
			port_serv, port_client = data_link.__send_frame(frame, destination_address, source_address, port_serv, port_client)
		else:
			nframes = (payload_len - 1) // 255 + 1
			sequence = (data_link.__SEQ_ONE, data_link.__SEQ_TWO)
			
			start, end = (0, 255)
			l_sdu_part = l_sdu.encode()[start:end].decode()
			frame = data_frame(sequence[0], destination_address, IPv4Address("0.0.0.0"), l_sdu_part)
			port_serv, port_client = data_link.__send_frame(frame, destination_address, source_address, port_serv, port_client)

			for i in range(1, nframes-1):
				start, end = (255*i, 255*(i+1))
				l_sdu_part = l_sdu.encode()[start:end].decode()
				frame = data_frame(sequence[i%2], destination_address, IPv4Address("0.0.0.0"), l_sdu_part)
				port_serv, port_client = data_link.__send_frame(frame, destination_address, source_address, port_serv, port_client)	
			
			start = 255*(nframes-1)
			l_sdu_part = l_sdu.encode()[start:].decode()
			frame = data_frame(data_link.__SEQ_LAST_FRAME, destination_address, IPv4Address("0.0.0.0"), l_sdu_part)
			port_serv, port_client = data_link.__send_frame(frame, destination_address, source_address, port_serv, port_client)	

	@staticmethod
	def __send_frame(frame, destination_address, source_address, port_serv, port_client):
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
			if n_ack == data_link.__NACK_ONE or n_ack == data_link.__NACK_TWO:
				resend = True
			else:
				resend = False
			
			physical_recv.close()

			port_client += 1
			port_serv += 1

		return port_serv, port_client

	@staticmethod
	def Data_Request(destination_address, source_address):
		port_serv = 12000
		port_client = 11000

		sequence = (data_link.__ACK_ONE, data_link.__ACK_TWO)
		frame, port_serv, port_client = data_link.__recv_frame(sequence[0], destination_address, source_address, port_serv, port_client)
		l_sdu = data_frame.bin_to_str(frame.get_payload())
		seq = frame.get_sequence()
		i = 1

		if seq != data_link.__SEQ_UNIQUE_FRAME:
			while seq != data_link.__SEQ_LAST_FRAME:
				frame, port_serv, port_client = data_link.__recv_frame(sequence[i%2], destination_address, source_address, port_serv, port_client)
				l_sdu += data_frame.bin_to_str(frame.get_payload())
				seq = frame.get_sequence()
				i += 1
		
		return l_sdu

	@staticmethod
	def __recv_frame(sequence, destination_address, source_address, port_serv, port_client):
		ack = ack_frame(sequence, destination_address, source_address)
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
				if sequence == data_link.__ACK_ONE:
					ack.set_sequence(data_link.__NACK_ONE) #nack
				else:
					ack.set_sequence(data_link.__NACK_TWO) #nack
				ack_bitstring = bin(ack.get_frame()).lstrip("0b")
				lenght_bin = len(ack_bitstring)
				for i in range(0, lenght_bin, 8):
					physical_send.F_Data_Indication(ack_bitstring[i:i+8], True)
				physical_send.close()

				response = True # precisa esperar outro frame
			
			ack.set_sequence(sequence) # apos enviar um nack voltar para ack
			port_client += 1
			port_serv += 1
		
		return frame_check, port_serv, port_client