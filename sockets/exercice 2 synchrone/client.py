import socket

client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 12345))

try:
    while True:
        message = input("Entrez votre message : ")
        client_socket.send(message.encode())
        if message.lower() == "bye":
            print("Déconnexion du client.")
            break
        elif message.lower() == "arret":
            print("Client arrêté et demande l'arrêt du serveur.")
            break
        reply = client_socket.recv(1024).decode()
        print(f"Réponse du serveur : {reply}")
except KeyboardInterrupt:
    print("Client arrêté par l'utilisateur.")
finally:
    client_socket.close()
