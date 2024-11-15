import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:  
                break
            print(f"Réponse du serveur : {message}")
        except OSError:  
            break

client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 1234))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

try:
    while True:
        message = input("Entrez votre message : ")
        client_socket.send(message.encode())
        if message.lower() in ["bye", "arret"]:
            print("Déconnexion du client.")
            client_socket.close()  
            break
except KeyboardInterrupt:
    print("Client arrêté par l'utilisateur.")
finally:
    client_socket.close()
