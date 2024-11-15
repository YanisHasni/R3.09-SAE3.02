import socket;

client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 1235))
print("Connexion au serveur")
message = "Bonjour serveur"
client_socket.send(message.encode())
reply = client_socket.recv(1024).decode()
client_socket.close()
