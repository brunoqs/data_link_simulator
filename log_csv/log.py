from time import localtime

from link_layer import ack_frame, data_frame

class log:
    """Classe responsável por gerar o log de eventos acontecidos na
    camada de enlace. Salva um arquivo no formato CSV."""

    # atributos privados estáticos - constantes:
    __SEP = ','   # separador de dados do arquivo (padrão CSV).
    __CRL = '\n'  # indicador de fim de linha (carry line).

    def __init__(self, path):
        """Construtor. Recebe o caminho 'path' do arquivo onde será
        salvo o log."""

        # atributo privado do objeto:
        self.__file = open(path, 'a') # abre o arquivo no modo append
        # porque o arquivo será aberto e fechado várias vezes, o que
        # permite que o log possa ser acompanhado em tempo real 
        # semelhante ao Wireshark. Se não estivesse no modo append,
        # o arquivo seria apagado toda vez.
    
    def clear(self):
        """Método que apaga o arquivo e deixa só o cabeçalho CSV nele."""

        # apaga o arquivo todo.
        self.__file.truncate(0)
        # escreve o cabeçalho nele.
        self.__file.write(
            'FRAME_TYPE' + 
            log.__SEP + 
            'EVENT' + 
            log.__SEP + 
            'DATE' + 
            log.__SEP + 
            'TIME' +
            log.__SEP + 
            'FRAME_HEX' + 
            log.__CRL
        )
    
    def close(self):
        """Método que fecha o arquivo de log para liberar o buffer."""
        self.__file.close()

    def __event(self, event, frame):
        """Método privado para escrever no arquivo de log."""
        
        if type(frame) == data_frame:
            ftype = 'data_frame'
        elif type(frame) == ack_frame:
            ftype = 'ack_frame'
        else:
            raise TypeError('frame is incorrect.')
        self.__file.write(
            ftype + 
            log.__SEP + 
            event + 
            log.__SEP + 
            self.__format_date(localtime()) + 
            log.__SEP + 
            self.__format_time(localtime()) +
            log.__SEP + 
            hex(frame.get_frame()) + 
            log.__CRL
        )

    def time_out(self, frame):
        """Método para registrar no log o evento.
        @param frame : data_frame | ack_frame"""
        self.__event('time_out', frame)
    
    def crc_error(self, frame):
        """Método para registrar no log o evento.
        @param frame : data_frame | ack_frame"""
        self.__event('crc_error', frame)
    
    def msg_sent(self, frame):
        """Método para registrar no log o evento.
        @param frame : data_frame | ack_frame"""
        self.__event('msg_sent', frame)
    
    def msg_recv(self, frame):
        """Método para registrar no log o evento.
        @param frame : data_frame | ack_frame"""
        self.__event('msg_recv', frame)
    
    def msg_retr(self, frame):
        """Método para registrar no log o evento.
        @param frame : data_frame | ack_frame"""
        self.__event('msg_retr', frame)

    def __format_time(self, time):
        """Método privado para obter a hora do sistema."""
        return '{:02d}:{:02d}:{:02d}'.format(time.tm_hour, time.tm_min, time.tm_sec)

    def __format_date(self, time):
        """Método privado para obter a data do sistema."""
        return '{}/{:02d}/{:02d}'.format(time.tm_year, time.tm_mon, time.tm_mday)