from link_layer import data_frame
from ipaddress import IPv4Address

def crc_check(input_bitstring, check_value, polynomial_bitstring='11000000000000101'):
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

        
def crc_remainder(input_bitstring, initial_filler='0', polynomial_bitstring='11000000000000101'):
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


################
################
################


x = data_frame(129, IPv4Address('255.255.255.255'), IPv4Address('255.255.255.255'), 'a')
print(x.crc_check())
