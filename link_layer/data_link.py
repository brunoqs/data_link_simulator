import time
from ipaddress import IPv4Address

from log_csv import log
from physical_layer import physical_link

from .ack_frame import ack_frame
from .data_frame import data_frame

class data_link:
    """Classe que simula a camada de enlace da rede.
    Todos os métodos são estáticos para se assemelhar ao Singleton,
    pois só existe um único enlace entre duas interfaces."""

    @staticmethod
    def Data_Indication(destination_address, source_address, l_sdu):
        """Método de primitiva de envio de uma cadeia de caracteres de tamanho arbitrário.
        @param destination_address : IPv4Address
        @param source_address : IPv4Address
        @param l_sdu : str"""

        logger = log('indication_log.csv') # abre o arquivo de log.
        logger.clear()                     # limpa o log para salvar só dados desta transmissão.
        logger.close()                     # fecha o log.

        port_serv = 11000   # porta inicial para socket server - envia dado.
        port_client = 12000 # porta inicial para socket client - recebe ack.

        payload_len = len(l_sdu.encode()) # tamanho tem que ser da string codificada (ex. 'ç' = 2 bytes).

        if payload_len <= 255:
            # envia só um quadro.
            frame = data_frame(data_frame.SEQ_UNIQUE_FRAME, destination_address, IPv4Address("0.0.0.0"), l_sdu)
            port_serv, port_client = data_link.__send_frame(frame, destination_address, source_address, port_serv, port_client)
        else:
            nframes = (payload_len - 1) // 255 + 1 # quantos quadros terá que enviar.
            sequence = (data_frame.SEQ_ONE, data_frame.SEQ_TWO) # para alternar o stop-and-wait, circular.
            
            # envia primeiro quadro.
            start, end = (0, 255) 
            l_sdu_part = l_sdu.encode()[start:end].decode()
            frame = data_frame(sequence[0], destination_address, IPv4Address("0.0.0.0"), l_sdu_part)
            port_serv, port_client = data_link.__send_frame(frame, destination_address, source_address, port_serv, port_client)

            for i in range(1, nframes-1):
                # envia segundo até o penúltimo quadro.
                start, end = (255*i, 255*(i+1))
                l_sdu_part = l_sdu.encode()[start:end].decode()
                frame = data_frame(sequence[i%2], destination_address, IPv4Address("0.0.0.0"), l_sdu_part)
                port_serv, port_client = data_link.__send_frame(frame, destination_address, source_address, port_serv, port_client)	
            
            # envia último quadro.
            start = 255*(nframes-1)
            l_sdu_part = l_sdu.encode()[start:].decode()
            frame = data_frame(data_frame.SEQ_LAST_FRAME, destination_address, IPv4Address("0.0.0.0"), l_sdu_part)
            port_serv, port_client = data_link.__send_frame(frame, destination_address, source_address, port_serv, port_client)	

    @staticmethod
    def __send_frame(frame, destination_address, source_address, port_serv, port_client):
        """Método privado para envio de um quadro através da camada física."""

        logger = log('indication_log.csv') # abre o arquivo de log.
        # log é acrescentado a cada quadro enviado, [n]ack recebido e retransmissões,
        # para ter uma visão completa do que aconteceu na camada de enlace, semelhante ao
        # Wireshark.
        
        logger.msg_sent(frame) # registra que um quadro foi enviado.
        resend = True
        while resend: # enquanto receber nack...
            # envia um quadro.
            physical_send = physical_link(destination_address, IPv4Address("0.0.0.0"), port_serv)
            frame_bitstring = bin(frame.get_frame()).lstrip("0b")
            lenght_bin = len(frame_bitstring)
            for i in range(0, lenght_bin, 8):
                physical_send.F_Data_Indication(frame_bitstring[i:i+8]) # envia de octeto em octeto.
            physical_send.close()

            # espera 1s para ficar esperando um ack ou nack.
            time.sleep(1)
            physical_recv = physical_link(destination_address, source_address, port_client)
            ack = ""
            flag = True
            while flag:
                request = physical_recv.F_Data_Request() # recebe quadro de [n]ack.
                if request:
                    ack += request.decode() 
                else:
                    flag = False

            # abre o quadro de [n]ack para ver seu sequence.
            ack_check = ack_frame(bin_flow_recv=int(ack, base=2)) 
            logger.msg_recv(ack_check) # registra quadro de ack/nack.
            n_ack = ack_check.get_sequence()
            if n_ack in (ack_frame.NACK_ONE, ack_frame.NACK_TWO):
                # quadro chegou corrompido, enviar outra vez.
                resend = True
                logger.msg_retr(frame) # registra retransmissão.
            else:
                # quadro chegou intacto, finalizar.
                resend = False
            
            physical_recv.close()

            # estratégia de alocar mais portas e não dar erro.
            port_client += 1
            port_serv += 1
        
        logger.close() # libera o buffer do log.

        return port_serv, port_client

    @staticmethod
    def Data_Request(destination_address, source_address):
        """Método de primitiva de recebimento de uma cadeia de caracteres.
        @param destination_address : IPv4Address
        @param source_address : IPv4Address
        @return str"""

        logger = log('request_log.csv') # abre o arquivo de log.
        logger.clear()                  # limpa o log para salvar só dados desta recepção.
        logger.close()                  # fecha o log.

        port_serv = 12000   # porta inicial para socket server - envia ack.
        port_client = 11000 # porta inicial para socket client - recebe dado.

        sequence = (ack_frame.ACK_ONE, ack_frame.ACK_TWO) # para alternar o stop-and-wait, circular.
        
        # recebe o primeiro quadro, envia ack ou nack.
        frame, port_serv, port_client = data_link.__recv_frame(sequence[0], destination_address, source_address, port_serv, port_client)
        l_sdu = data_frame.bin_to_str(frame.get_payload())
        seq = frame.get_sequence()
        i = 1

        if seq != data_frame.SEQ_UNIQUE_FRAME:
            # recebe os próximos quadros, envia ack ou nack.
            while seq != data_frame.SEQ_LAST_FRAME:
                frame, port_serv, port_client = data_link.__recv_frame(sequence[i%2], destination_address, source_address, port_serv, port_client)
                l_sdu += data_frame.bin_to_str(frame.get_payload())
                seq = frame.get_sequence()
                i += 1
        
        return l_sdu # mensagem recebida

    @staticmethod
    def __recv_frame(sequence, destination_address, source_address, port_serv, port_client):
        """Método privado para recepção de um quadro através da camada física."""

        logger = log('request_log.csv') # abre o arquivo de log.
        # log é acrescentado a cada quadro recebido e [n]ack enviado,
        # para ter uma visão completa do que aconteceu na camada de enlace, semelhante ao
        # Wireshark.

        ack = ack_frame(sequence, destination_address, source_address)
        response = True
        while response: # enquanto tiver que esperar outro pacote...
            # espera o quadro.
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

            # espera 2s para enviar um ack após abrir o quadro e testar o CRC.
            time.sleep(2)
            physical_send = physical_link(destination_address, IPv4Address("0.0.0.0"), port_serv)
            frame_check = data_frame(bin_flow_recv=int(frame, base=2))
            logger.msg_recv(frame_check) # registra quadro recebido.

            if frame_check.crc_check():
                # crc = True, envia ack.
                logger.msg_sent(ack)
                ack_bitstring = bin(ack.get_frame()).lstrip("0b")
                lenght_bin = len(ack_bitstring)
                for i in range(0, lenght_bin, 8):
                    physical_send.F_Data_Indication(ack_bitstring[i:i+8], True)
                physical_send.close()

                response = False # não precisa esperar outro quadro.
            else:
                # crc = False, envia nack.
                logger.crc_error(frame_check) # registra quadro corrompido.
                if sequence == ack_frame.ACK_ONE:
                    ack.set_sequence(ack_frame.NACK_ONE) # nack
                else:
                    ack.set_sequence(ack_frame.NACK_TWO) # nack
                ack_bitstring = bin(ack.get_frame()).lstrip("0b")
                lenght_bin = len(ack_bitstring)
                for i in range(0, lenght_bin, 8):
                    physical_send.F_Data_Indication(ack_bitstring[i:i+8], True)
                physical_send.close()

                response = True # precisa esperar outro quadro.
            
            ack.set_sequence(sequence) # após enviar um nack voltar para ack.

            # estratégia de alocar mais portas e não dar erro.
            port_client += 1
            port_serv += 1
        
        logger.close() # libera buffer do log.
        
        # python não tem passagem por referência de tipo primitivo, tem que retornar.
        return frame_check, port_serv, port_client # quadro e próximas portas