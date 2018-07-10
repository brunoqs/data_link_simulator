# COLOCAR PAYLOAD EM <class 'str'>

class data_frame:
    def __init__(self, bin_flow_recv):
        self.__bin =  bin_flow_recv

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
    
    def __str_to_bin(self, payload):
        return int(bytes(payload, encoding='utf-8').hex(), base=16)

    def __bin_to_str(self, payload):
        return bytearray.fromhex(hex(payload).lstrip('0x')).decode('utf-8')

    def __gen_crc(self, message):
        return 0x0000

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
