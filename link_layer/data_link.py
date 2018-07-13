from .data_frame import data_frame
from .ack_frame import ack_frame

from physical_layer import physical_link

from ipaddress import IPv4Address 

import time

class data_link:
	@staticmethod
	def Data_Request(destination_address, l_sdu):
		if type(destination_address) != IPv4Address:
			raise TypeError('destination_address must be IPv4Address.')
		if type(l_sdu) != str:
			raise TypeError('l_sdu must be str.')
		
		physical_send = physical_link(destination_address, port=11000)

		l_sdu_bytes = l_sdu.encode('utf-8')

		if len(l_sdu_bytes) < 256:
			frame = data_frame(0b00000000, destination_address, l_sdu)
			frame_bitstring = bin(frame.get_frame()).lstrip("0b")
			lenght_bin = len(frame_bitstring)
			for i in range(0, lenght_bin, 8):
				physical_send.F_Data_Request(frame_bitstring[i:i+8])
			physical_send.fin_data()
			physical_send.close()
		else:
			nframes = ((len(l_sdu_bytes) - 1) // 255) + 1
			for i in range(nframes - 1):
				frame = data_frame(0b00000000, destination_address, l_sdu_bytes[(255*i) : 255*(i+1)-1].decode('utf-8'))
				frame_bitstring = bin(frame.get_frame()).lstrip("0b")
				lenght_bin = len(frame_bitstring)
				for i in range(0, lenght_bin, 8):
					physical_send.F_Data_Request(frame_bitstring[i:i+8])
				physical_send.fin_data()
				physical_send.close()

				time.sleep(1)
				physical_recv = physical_link(destination_address, IPv4Address("127.0.0.1"), 12000)
				ack = ""
				flag = True
				while flag:
					request = physical_recv.F_Data_Indication()
					print(request.decode())
					if request != "".encode():
						ack += request.decode()
					else:
						flag = False
				print(ack)
				physical_recv.close()

	@staticmethod
	def Data_Indication(destination_address, source_address):
		ack = ack_frame(0, destination_address, source_address)
		
		physical_recv = physical_link(destination_address, source_address, 11000)
		frame = ""
		flag = True
		while flag:
			request = physical_recv.F_Data_Indication()
			print(request.decode())
			if request != "".encode():
				frame += request.decode()
			else:
				flag = False
		print (frame)
		physical_recv.close()

		time.sleep(2)
		physical_send = physical_link(destination_address, IPv4Address("0.0.0.0"), 12000)
		frame_check = data_frame(bin_flow_recv=int(frame, base=2))
		if frame_check.crc_check():
			ack_bitstring = bin(ack.get_frame()).lstrip("0b")
			lenght_bin = len(ack_bitstring)
			for i in range(0, lenght_bin, 8):
				physical_send.F_Data_Request(ack_bitstring[i:i+8])
			physical_send.fin_data()
			physical_send.close()
