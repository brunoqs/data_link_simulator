# COLOCAR PAYLOAD EM <class 'str'>

from data_frame import data_frame

class data_frame_server(data_frame):
    def __init__(self, sequence, destination_address, source_address, payload):
        lenght = len(payload) & 0xFF # 1 byte
        sequence &= 0xFF # 1 byte
        destination_address &= 0xFFFFFFFF # 4 bytes
        source_address &= 0xFFFFFFFF # 4 bytes
        payload = self.__str_to_bin(payload) # 'lenght' bytes, 0 <= 'lenght' <= 255
        crc = self.__gen_crc(
            lenght << ((9 + lenght) * 8) | \
            sequence << ((8 + lenght) * 8) | \
            destination_address << ((4 + lenght) * 8) | \
            source_address << (lenght * 8) | \
            payload
        ) # 2 bytes

        super().__init__(
            (0x7E << ((12 + lenght) * 8)) | \
            (lenght << ((11 + lenght) * 8)) | \
            (sequence << ((10 + lenght) * 8)) | \
            (destination_address << ((6 + lenght) * 8)) | \
            (source_address << ((2 + lenght) * 8)) | \
            (payload << 16) | \
            (crc)
        )