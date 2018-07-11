#
# testado 100% ok
#

from ipaddress import IPv4Address

class ack_frame():
    __DEL = 0x7E

    def __init__(self, sequence, destination_address, source_address):
        if type(sequence) != int:
            raise TypeError('sequence must be int.')
        if type(destination_address) != IPv4Address:
            raise TypeError('destination_address must be IPv4Address.')
        if type(source_address) != IPv4Address:
            raise TypeError('source_address must be IPv4Address.')
        if sequence & 0b01111110 != 0:
                raise ValueError('sequence is wrong.')
        
        sequence &= 0xFF # 1 byte
        destination_address = int(destination_address) # 4 bytes
        source_address = int(source_address) # 4 bytes

        self.__bin =  \
            (self.__DEL << 72) | \
            (sequence << 64) | \
            (destination_address << 32) | \
            (source_address)
    
    def get_frame(self):
        return self.__bin
    
    def get_sequence(self):
        return (self.__bin >> 64) & 0xFF
    
    def get_destination_addr(self):
        return (self.__bin >> 32) & 0xFFFFFFFF
    
    def get_source_addr(self):
        return self.__bin & 0xFFFFFFFF
    