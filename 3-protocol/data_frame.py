class data_frame:
    def __init__(self, sequence, destination_address, source_address, payload):
        n = len(payload)
        self.__bin =  \
            (0x7E << ((11 + n) * 8)) | \
            (sequence << ((10 + n) * 8)) | \
            (destination_address << ((6 + n) * 8)) | \
            (source_address << ((2 + n) * 8)) | \
            (str_to_bin(payload) << 16) | \
            (crc(0))

        self.__lenght = None # 1 byte
        self.__sequence = sequence # 1 byte
        self.__destination_address = destination_address # 4 bytes
        self.__source_address = source_address # 4 bytes
        self.__payload = payload # n bytes, 0 <= n <= 255
        self.__crc = None # 2 bytes

        # COLOCAR PAYLOAD EM <class 'str'>
    
def str_to_bin(payload):
	return int(bytes(payload, encoding='utf-8').hex(), base=16)

def bin_to_str(payload):
	return bytearray.fromhex(hex(payload).lstrip('0x')).decode('utf-8')

def crc(frame):
    return 0

'''

payload : <class 'str'>

str_to_bin..

int(bytes(payload, encoding='utf-8').hex(), base=16)

------------------------------------------------------------

payload : <class 'int'>

bin_to_str..

bytearray.fromhex(hex(payload).lstrip('0x')).decode('utf-8')

'''