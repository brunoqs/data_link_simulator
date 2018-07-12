#
# testado 100% ok
#

from ipaddress import IPv4Address

class data_frame(object):
    __DEL = 0x7E
    __POLYNOM_GEN = 0b11000000000000101

    def __init__(self, sequence=None, destination_address=None, source_address=None, payload=None, bin_flow_recv=None):
        if bin_flow_recv != None:
            if type(bin_flow_recv) != int:
                raise TypeError('bin_flow_recv must be int.')

            self.__bin =  bin_flow_recv
        else:
            if type(sequence) != int:
                raise TypeError('sequence must be int.')
            if type(destination_address) != IPv4Address:
                raise TypeError('destination_address must be IPv4Address.')
            if type(source_address) != IPv4Address:
                raise TypeError('source_address must be IPv4Address.')
            if type(payload) != str:
                raise TypeError('payload must be str.')
            if len(bytes(payload, encoding='utf-8')) > 255:
                raise ValueError('payload lenght must be max 255.')
            if sequence & 0b01111110 != 0:
                raise ValueError('sequence is wrong.')

            lenght = len(bytes(payload, encoding='utf-8')) # 1 byte
            sequence &= 0xFF # 1 byte
            destination_address = int(destination_address) # 4 bytes
            source_address = int(source_address) # 4 bytes
            payload = data_frame.str_to_bin(payload) # 'lenght' bytes, 0 <= 'lenght' <= 255
            
            crc_arg =  \
                lenght << ((9 + lenght) * 8) | \
                sequence << ((8 + lenght) * 8) | \
                destination_address << ((4 + lenght) * 8) | \
                source_address << (lenght * 8) | \
                payload
            
            crc = self.__crc_gen(crc_arg) # 2 bytes

            self.__bin =  \
                (self.__DEL << ((12 + lenght) * 8)) | \
                (lenght << ((11 + lenght) * 8)) | \
                (sequence << ((10 + lenght) * 8)) | \
                (destination_address << ((6 + lenght) * 8)) | \
                (source_address << ((2 + lenght) * 8)) | \
                (payload << 16) | \
                (crc)

    def set_frame(self, bin):
        self.__bin = bin

    def get_frame(self):
        return self.__bin
    
    def get_lenght(self):
        n = self.__bin.bit_length() - 15 # -16+1 = 15, pq 0x7E = 0111 1110, 0 a esq. descarta na cpu
        return (self.__bin >> n) & 0xFF

    def get_sequence(self):
        n = self.__bin.bit_length() - 23
        return (self.__bin >> n) & 0xFF
    
    def get_destination_addr(self):
        n = self.__bin.bit_length() - 55
        return (self.__bin >> n) & 0xFFFFFFFF
    
    def get_source_addr(self):
        n = self.__bin.bit_length() - 87
        return (self.__bin >> n) & 0xFFFFFFFF
    
    def get_payload(self):
        lenght = self.get_lenght() * 8
        return (self.__bin >> 16) & ((1 << lenght) - 1)
    
    def get_crc(self):
        return self.__bin & 0xFFFF
    
    @staticmethod
    def str_to_bin(payload):
        return int(bytes(payload, encoding='utf-8').hex(), base=16)

    @staticmethod
    def bin_to_str(payload):
        return bytearray.fromhex(hex(payload).lstrip('0x')).decode('utf-8')

    def __crc_gen(self, message):
        bitstring = bin(message).lstrip('0b')
        polynom = bin(self.__POLYNOM_GEN).lstrip('0b')
        crc_bitstring = self.__crc_remainder(bitstring, polynom, '0')
        return int(crc_bitstring, base=2)
    
    def crc_check(self):
        bitstring_frame = bin(self.__bin).lstrip('0b')
        bitstring = bitstring_frame[8:-16]
        polynom = bin(self.__POLYNOM_GEN).lstrip('0b')
        check = bitstring_frame[-16:]
        return self.__crc_check(bitstring, polynom, check)

    def __crc_check(self, input_bitstring, polynomial_bitstring, check_value):
        '''
        Calculates the CRC check of a string of bits using a chosen polynomial.
        initial_filler should be '1' or '0'.
        '''
        len_input = len(input_bitstring)
        initial_padding = check_value
        input_padded_array = list(input_bitstring + initial_padding)
        polynomial_bitstring = polynomial_bitstring.lstrip('0')
        while '1' in input_padded_array[:len_input]:
            cur_shift = input_padded_array.index('1')
            for i in range(len(polynomial_bitstring)):
                if polynomial_bitstring[i] == input_padded_array[cur_shift + i]:
                    input_padded_array[cur_shift + i] = '0'
                else:
                    input_padded_array[cur_shift + i] = '1'
        if '1' not in ''.join(input_padded_array)[len_input:]:
            return True
        else:
            return False 
    
    def __crc_remainder(self, input_bitstring, polynomial_bitstring, initial_filler):
        '''
        Calculates the CRC remainder of a string of bits using a chosen polynomial.
        initial_filler should be '1' or '0'.
        '''
        len_input = len(input_bitstring)
        initial_padding = initial_filler * (len(polynomial_bitstring) - 1)
        input_padded_array = list(input_bitstring + initial_padding)
        polynomial_bitstring = polynomial_bitstring.lstrip('0')
        while '1' in input_padded_array[:len_input]:
            cur_shift = input_padded_array.index('1')
            for i in range(len(polynomial_bitstring)):
                if polynomial_bitstring[i] == input_padded_array[cur_shift + i]:
                    input_padded_array[cur_shift + i] = '0'
                else:
                    input_padded_array[cur_shift + i] = '1'
        return ''.join(input_padded_array)[len_input:]
