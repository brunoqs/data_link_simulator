class data_frame:
    __DELIMITER = 0x7E # 1 byte

    def __init__(self, sequence, destination_address, source_address, payload):
        self.__lenght = None # 1 byte
        self.__sequence = sequence # 1 byte
        self.__destination_address = destination_address # 4 bytes
        self.__source_address = source_address # 4 bytes
        self.__payload = payload # n bytes, 0 <= n <= 255
        self.__crc = None # 2 bytes