import socket
import threading
import sys

# Configuration du serveur
host = '0.0.0.0'
port = 1234
clients = []
server_running = True  # Drapeau pour indiquer si le serveur est en cours d'exécution

# Fonction pour gérer chaque client
def handle_client(conn, address):
    global server_running
    print(f"Connexion de {address}")
    clients.append((conn, address))
    
    while server_running:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break

            print(f"Message reçu de {address}: {message}")

            if message.lower() == "bye":
                reply = "Déconnexion du client"
                conn.send(reply.encode())
                break
            elif message.lower() == "arret":
                reply = "Arrêt du serveur et des clients"
                conn.send(reply.encode())
                server_running = False  # Mettre le drapeau à False pour arrêter le serveur
                break
            else:
                broadcast_message = f"{address[0]}: {message}"
                for client in clients:
                    if client[0] != conn:
                        client[0].send(broadcast_message.encode())
        
        except:
            break

    conn.close()
    clients.remove((conn, address))
    print(f"Client {address} déconnecté")

# Fonction pour arrêter le serveur proprement
def stop_server():
    global server_running
    server_running = False
    print("Fermeture du serveur...")
    for client in clients:
        client[0].close()
    server_socket.close()
    sys.exit()

# Création du socket
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Réutilisation de l'adresse
server_socket.bind((host, port))
server_socket.listen(5)

print("Serveur en attente de connexions...")

# Boucle principale pour accepter les connexions
try:
    while server_running:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()
except KeyboardInterrupt:
    stop_server()

# Arrêter le serveur de manière propre lorsque le drapeau est False
if not server_running:
    stop_server()
