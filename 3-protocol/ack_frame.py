class ack_frame:
    __DELIMITER = 0x7E # 1 byte

    def __init__(self, sequence, destination_address, source_address):
        self.__sequence = sequence # 1 byte
        self.__destination_address = destination_address # 4 bytes
        self.__source_address = source_address # 4 bytes