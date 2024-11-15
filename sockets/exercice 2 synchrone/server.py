import socket

server_socket = socket.socket()
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(5)
print("Serveur en attente de connexions...")

try:
    while True:
        conn, address = server_socket.accept()
        print(f"Connexion acceptée de {address}")

        while True:
            message = conn.recv(1024).decode()
            if message.lower() == "bye":
                print(f"Client {address} déconnecté.")
                conn.close()
                break  
            elif message.lower() == "arret":
                print("Arrêt du serveur.")
                conn.close()
                server_socket.close()
                exit()
            else:
                print(f"Message reçu : {message}")
                reply = input("Entrez votre réponse : ")
                conn.send(reply.encode())
except KeyboardInterrupt:
    print("Serveur arrêté par l'utilisateur.")
finally:
    server_socket.close()
