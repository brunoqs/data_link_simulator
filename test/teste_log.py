from log_csv import log
from link_layer import data_frame
from link_layer import ack_frame
from ipaddress import IPv4Address

data = data_frame(0, IPv4Address('0.0.0.0'), IPv4Address('0.0.0.0'), 'kasinão')
ack = ack_frame(0, IPv4Address('0.0.0.0'), IPv4Address('0.0.0.0'))

arq = log('log_teste.csv')

arq.time_out(data)
arq.time_out(ack) 
arq.crc_error(data)
arq.crc_error(ack)
arq.msg_sent(data)
arq.msg_sent(ack)
arq.msg_recv(data)
arq.msg_recv(ack)
arq.msg_retr(data)
arq.msg_retr(ack)

arq.close()
