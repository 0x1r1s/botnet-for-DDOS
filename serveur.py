# Script serveur
import argparse
import socket
from cryptography.fernet import Fernet


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

parser = argparse.ArgumentParser(prog="botnet DDoS", description="A botnet DDoS in python")

parser.add_argument("ip_address", type=str, help="The IP address of the victim")
parser.add_argument("-b", "--bitrate", type=int, help="The bitrate for the attack in MB/s", action="store")
parser.add_argument("-t", "--time", type=int, help="The length of the attack in second", action="store")

args = parser.parse_args() # Access args with args.ip_address, args.bitrate, args.time

#Récupération de la clé symétrique
with open("secret.key", "rb") as key_file:
    key=key_file.read()
fernet = Fernet(key)

# Création d'un socket en utilisant l'IPv4 et le protocole TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liaison du socket à une adresse IP et un port
HOST="localhost"
PORT=8081
server_socket.bind((HOST, PORT))

# Ecoute des connexions entrantes
server_socket.listen()

# Acceptation d'une connexion avec le client
client_socket, client_address = server_socket.accept()
print("Accepted a connection request from %s:%s"%(client_address[0], client_address[1]))

# Envoi des données au client
encrypted_data=fernet.encrypt(b"Hello Client")
client_socket.send(encrypted_data)


# Fermeture de la connexion avec le client
client_socket.close()

# Fermeture du socket serveur   
server_socket.close()