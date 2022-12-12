# Script client
import socket
from cryptography.fernet import Fernet

#Récupération de la clé symétrique
with open("secret.key", "rb") as key_file:
    key=key_file.read()
fernet = Fernet(key)

# Création d'un socket en utilisant l'IPv4 et le protocole TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
HOST="localhost"
PORT=8081
client_socket.connect((HOST, PORT))

# Réception des données du serveur
encrypted_data = client_socket.recv(1024)
print(encrypted_data,"\n")
decrypted_data=fernet.decrypt(encrypted_data)

# Affichage des données reçues
print(decrypted_data)

# Fermeture du socket client
client_socket.close()