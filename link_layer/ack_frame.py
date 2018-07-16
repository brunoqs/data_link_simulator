from ipaddress import IPv4Address

class ack_frame:
    """Classe que implementa o quadro de ACK."""

    # atributo privado estático - constante:
    __DEL = 0x7E # delimitador do quadro

    # atributos públicos estático - constante:
    # o programador tem que ter bom senso de não mudar o valor, python não tem como colocar 'const'.
    ACK_ONE = 0b00000001  # sequence stop-and-wait ack
    ACK_TWO = 0b10000001  # sequence stop-and-wait ack
    NACK_ONE = 0b00000000 # sequence stop-and-wait nack
    NACK_TWO = 0b10000000 # sequence stop-and-wait nack

    def __init__(self, sequence=None, destination_address=None, source_address=None, bin_flow_recv=None):
        """Construtor.
        Se for construir um quadro novo, usar somente os 3 primeiros parâmetros.
        Se for construir um quadro a partir de um binário já criado, usar somente o último parâmetro.
        @param sequence : int (default None)
        @param destination_address : IPv4Address (default None)
        @param source_address : IPv4Address (default None)
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
            if sequence & 0b01111110 != 0:
                raise ValueError('sequence is wrong.')
            
            # aplica máscara para restringir o tamanho dos campos.
            sequence &= 0xFF # 1 byte
            destination_address = int(destination_address) # 4 bytes
            source_address = int(source_address) # 4 bytes

            # atributo privado do objeto:
            # constrói o quadro em binário usando operações bitwise
            # para fazer a concatenação.
            self.__bin =  \
                (self.__DEL << 72) | \
                (sequence << 64) | \
                (destination_address << 32) | \
                (source_address)
        
    def get_frame(self):
        """Método que retorna quadro em binário.
        @return int"""
        return self.__bin
    
    def set_sequence(self, sequence):
        """Método que modifica o valor de sequence no quadro.
        @param sequence : int"""

        if sequence & 0b01111110 != 0:
            raise ValueError('sequence is wrong.')

        self.__bin &= ((0xFF << 72) | 0xFFFFFFFFFFFFFFFF)
        self.__bin |= ((sequence << 64) | 0xFFFFFFFFFFFFFFFF)
    
    def get_sequence(self):
        """Método que retorna o valor (binário) de sequence do quadro.
        @return int"""
        return (self.__bin >> 64) & 0xFF
    
    def get_destination_addr(self):
        """Método que retorna o valor (binário) de destination address do quadro.
        @return int"""
        return (self.__bin >> 32) & 0xFFFFFFFF
    
    def get_source_addr(self):
        """Método que retorna o valor (binário) de source address do quadro.
        @return int"""
        return self.__bin & 0xFFFFFFFF