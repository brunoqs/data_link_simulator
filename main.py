import threading

from link_layer import data_link

x = data_link.data_link()

t = threading.Thread(target=x.Data_Indication,args=("", "", ""))
t.start()

x.Data_Request("","")
