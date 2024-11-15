import socket
import threading

def handle_client(conn, address):
    print(f"Connexion acceptée de {address}")
    try:
        while True:
            message = conn.recv(1024).decode()
            if message.lower() == "bye":
                print(f"Client {address} déconnecté.")
                conn.close()
                break
            elif message.lower() == "arret":
                print("Arrêt du serveur.")
                conn.close()
                for client in clients:
                    client.close()
                server_socket.close()
                exit()
            else:
                print(f"Message de {address} : {message}")
                reply = "Message reçu"
                conn.send(reply.encode())
    except ConnectionResetError:
        print(f"Client {address} déconnecté.")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 1234))
server_socket.listen(5)
print("Serveur en attente de connexions...")

clients = []

try:
    while True:
        conn, address = server_socket.accept()
        clients.append(conn)
        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()
except KeyboardInterrupt:
    print("Serveur arrêté par l'utilisateur.")
finally:
    for client in clients:
        client.close()
    server_socket.close()
