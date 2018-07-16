from link_layer import data_link
from ipaddress import IPv4Address

# Aqui o usuário na outra ponta do enlace recebe a mensagem que está enviada a ele, o 'l_sdu'.
# Para isso, usa a primitiva da camada de enlace (data_link) que será responsável por ficar
# escutando a rede e retornar os dados entregues. Por causa de adversidades na rede, alguns 
# quadros podem ficar comprometidos, mas isso é invisível ao usuário, sendo que a camada de enlace
# deste lado comunica quando houve erros e pede o quadro novamente. Caso esteja tudo correto, comunica
# que pode enviar o próximo quadro.

# Para teste entre 'localhost' <--> 'localhost'.
l_sdu = data_link.Data_Request(IPv4Address("127.0.0.1"), IPv4Address("127.0.0.1"))

# Para teste na VM rodando 'request.py'. VM que recebe é o ip '192.168.0.100'.
# l_sdu = data_link.Data_Request(IPv4Address("192.168.0.107"), IPv4Address("192.168.0.100"))

# Imprime no console a mensagem recebida.
print('RECEIVED:', l_sdu)

# Ao final da execução, o arquivo 'request_log.csv' conterá todos os detalhes que aconteceram
# na camada de enlace da interface receptora.