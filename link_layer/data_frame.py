from ipaddress import IPv4Address

class data_frame(object):
    """Classe que implementa o quadro de dados."""

    # atributos privados estáticos - constantes:
    __DEL = 0x7E                        # delimitador do quadro
    __POLYNOM_GEN = 0b11000000000000101 # polinômio gerador do CRC

    # atributos públicos estáticos - constantes:
    # o programador tem que ter bom senso de não mudar o valor, python não tem como colocar 'const'.
    SEQ_ONE = 0b00000000          # sequence stop-and-wait
    SEQ_TWO = 0b10000000          # sequence stop-and-wait
    SEQ_UNIQUE_FRAME = 0b00000001 # indica quadro único
    SEQ_LAST_FRAME = 0b10000001   # indica o último quadro enviado

    def __init__(self, sequence=None, destination_address=None, source_address=IPv4Address('0.0.0.0'), payload=None, bin_flow_recv=None):
        """Construtor.
        Se for construir um quadro novo, usar somente os 4 primeiros parâmetros.
        Se for construir um quadro a partir de um binário já criado, usar somente o último parâmetro.
        @param sequence : int (default None)
        @param destination_address : IPv4Address (default None)
        @param source_address : IPv4Address (default None)
        @param payload : str (default None)
        @param bin_flow_recv : int (default None)"""

        # como em python não tem sobrecarga de métodos, assim que será feito.
        if bin_flow_recv != None:
            # corretude de parâmetro.
            if type(bin_flow_recv) != int:
                raise TypeError('bin_flow_recv must be int.')
            # atributo privado do objeto:
            self.__bin =  bin_flow_recv # quadro inteiro em binário (int)
            # python o int tem comprimento de bits 'infinito', então a 
            # estrutura é possível sem usar array.
        else:
            # corretude de parâmetros.
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

            # aplica máscara para restringir o tamanho dos campos.
            lenght = len(bytes(payload, encoding='utf-8')) # 1 byte
            sequence &= 0xFF # 1 byte
            destination_address = int(destination_address) # 4 bytes
            source_address = int(source_address) # 4 bytes
            payload = data_frame.str_to_bin(payload) # 'lenght' bytes, 0 <= 'lenght' <= 255
            
            # argumento para cálculo do CRC, composto por tudo exceto o delimitador.
            crc_arg =  \
                lenght << ((9 + lenght) * 8) | \
                sequence << ((8 + lenght) * 8) | \
                destination_address << ((4 + lenght) * 8) | \
                source_address << (lenght * 8) | \
                payload
            
            crc = self.__crc_gen(crc_arg) # 2 bytes

            # atributo privado do objeto:
            # constrói o quadro em binário usando operações bitwise
            # para fazer a concatenação.
            self.__bin =  \
                (self.__DEL << ((12 + lenght) * 8)) | \
                (lenght << ((11 + lenght) * 8)) | \
                (sequence << ((10 + lenght) * 8)) | \
                (destination_address << ((6 + lenght) * 8)) | \
                (source_address << ((2 + lenght) * 8)) | \
                (payload << 16) | \
                (crc)

    def get_frame(self):
        """Método que retorna quadro em binário.
        @return int"""
        return self.__bin
    
    def get_lenght(self):
        """Método que retorna o valor (binário) do tamanho do payload.
        @return int"""
        n = self.__bin.bit_length() - 15 # -16+1 = 15, pq 0x7E = 0111 1110, 0 a esq. descarta
        return (self.__bin >> n) & 0xFF

    def get_sequence(self):
        """Método que retorna o valor (binário) de sequence do quadro.
        @return int"""
        n = self.__bin.bit_length() - 23
        return (self.__bin >> n) & 0xFF
    
    def get_destination_addr(self):
        """Método que retorna o valor (binário) de destination address do quadro.
        @return int"""
        n = self.__bin.bit_length() - 55
        return (self.__bin >> n) & 0xFFFFFFFF
    
    def get_source_addr(self):
        """Método que retorna o valor (binário) de source address do quadro.
        @return int"""
        n = self.__bin.bit_length() - 87
        return (self.__bin >> n) & 0xFFFFFFFF
    
    def get_payload(self):
        """Método que retorna o valor (binário) do payload do quadro.
        @return int"""
        lenght = self.get_lenght() * 8
        return (self.__bin >> 16) & ((1 << lenght) - 1)
    
    def get_crc(self):
        """Método que retorna o valor (binário) do CRC quadro.
        @return int"""
        return self.__bin & 0xFFFF
    
    @staticmethod
    def str_to_bin(payload):
        """Método estático que converte payload string para binário.
        @param payload : str
        @return bin"""
        return int(bytes(payload, encoding='utf-8').hex(), base=16)

    @staticmethod
    def bin_to_str(payload):
        """Método estático que converte payload binário para string.
        @param payload : int
        @return str"""
        return bytearray.fromhex(hex(payload).lstrip('0x')).decode('utf-8')

    def __crc_gen(self, message):
        """Método privado para cálculo do CRC. Chama outro método de terceiros, usando
        Padrão de Projeto Adapter."""

        bitstring = bin(message).lstrip('0b')
        polynom = bin(self.__POLYNOM_GEN).lstrip('0b')
        crc_bitstring = self.__crc_remainder(bitstring, polynom, '0')
        return int(crc_bitstring, base=2)
    
    def crc_check(self):
        """Método para verificação do CRC. Chama outro método de terceiros, usando
        Padrão de Projeto Adapter.
        @return bool"""

        bitstring_frame = bin(self.__bin).lstrip('0b')
        bitstring = bitstring_frame[7:-16] # 7 pq 0 no inicio do 0x7E desloca a string
        polynom = bin(self.__POLYNOM_GEN).lstrip('0b')
        check = bitstring_frame[-16:]
        return self.__crc_check(bitstring, polynom, check)

    def __crc_check(self, input_bitstring, polynomial_bitstring, check_value):
        '''Calculates the CRC check of a string of bits using a chosen polynomial.
        initial_filler should be '1' or '0'.
        @link https://en.wikipedia.org/wiki/Cyclic_redundancy_check'''
        
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
        '''Calculates the CRC remainder of a string of bits using a chosen polynomial.
        initial_filler should be '1' or '0'.
        @link https://en.wikipedia.org/wiki/Cyclic_redundancy_check'''

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