import socket

host = '0.0.0.0'  
port = 1234

while True:
    client_socket = socket.socket()
    client_socket.connect((host, port))
    
    message = input("Entrez votre message (bye pour quitter, arret pour arrêter le serveur) : ")
    client_socket.send(message.encode())
    
    reply = client_socket.recv(1024).decode()
    print(f"Réponse du serveur: {reply}")
    
    client_socket.close()
    
    if message.lower() in ["bye", "arret"]:
        break
