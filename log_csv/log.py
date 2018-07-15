from time import localtime

from link_layer import data_frame
from link_layer import ack_frame

class log:
    __SEP = ','
    __CRL = '\n'

    def __init__(self, path):
        self.__file = open(path, 'a')
    
    def clear(self):
        self.__file.truncate(0)
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
        self.__file.close()

    def __event(self, event, frame):
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
        self.__event('time_out', frame)
    
    def crc_error(self, frame):
        self.__event('crc_error', frame)
    
    def msg_sent(self, frame):
        self.__event('msg_sent', frame)
    
    def msg_recv(self, frame):
        self.__event('msg_recv', frame)
    
    def msg_retr(self, frame):
        self.__event('msg_retr', frame)

    def __format_time(self, time):
        return '{:02d}:{:02d}:{:02d}'.format(time.tm_hour, time.tm_min, time.tm_sec)

    def __format_date(self, time):
        return '{}/{:02d}/{:02d}'.format(time.tm_year, time.tm_mon, time.tm_mday)

        