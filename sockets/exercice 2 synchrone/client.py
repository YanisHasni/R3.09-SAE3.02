import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 1234))

try:
    while True:
        message = input("Entrez votre message : ")
        client_socket.send(message.encode())
        if message.lower() in ["bye", "arret"]:
            print("Déconnexion du client.")
            break
        reply = client_socket.recv(1024).decode()
        print(f"Réponse du serveur : {reply}")
except KeyboardInterrupt:
    print("Client arrêté par l'utilisateur.")
finally:
    client_socket.close()
