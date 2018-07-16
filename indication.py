from link_layer import data_link
from ipaddress import IPv4Address

# 'l_sdu' é uma string de tamanho arbitrário que o usuário deseja enviar ao outro
# host. Aqui ele digita essa mensagem.
l_sdu = input('SENDING: ')

# Próximo passo é invocar a primitiva do enlace de dados (data_link) que será responsável
# por enviar os dados do usuário 'l_sdu' para o destino. O quadro do protocolo implementado
# aceita o payload com no máximo 255 bytes (por exemplo, 'ç' são 2 bytes), então se o 'l_sdu'
# for maior do que isso, a camada de enlace deverá criar vários quadros para poder entregar
# a mensagem completa ao destino, mas isso é invisível no nível da aplicação, que é este nível.
# Também podem acontecer erros de transmissão na camada física (physical_link), que também não
# podem atrapalhar a confiabilidade do protocolo implementado.
# Aqui é garantido que qualquer cadeia de caracteres será entregue ao destino.

# Para teste entre 'localhost' <--> 'localhost'.
data_link.Data_Indication(IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1"), l_sdu)

# Para teste na VM rodando 'indication.py'. VM que envia é o ip '192.168.0.107'.
# data_link.Data_Indication(IPv4Address("192.168.0.100"), IPv4Address("192.168.0.107"), l_sdu)

# Ao final da execução, o arquivo 'indication_log.csv' conterá todos os detalhes que aconteceram
# na camada de enlace da interface transmissora.