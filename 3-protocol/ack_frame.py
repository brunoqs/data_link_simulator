class ack_frame:
    def __init__(self, sequence, destination_address, source_address):
        self.__bin =  (0x7E << 72) | (sequence << 64) | (destination_address << 32) | (source_address)
        #             1 byte           1 byte                   4 bytes                  4 bytes
    
    def get_sequence(self):
        return (self.__bin >> 64) & 0xFF
    
    def get_destination_addr(self):
        return (self.__bin >> 32) & 0xFFFFFFFF
    
    def get_source_addr(self):
        return self.__bin & 0xFFFFFFFF