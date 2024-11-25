import socket
import threading

def handle_client(conn, address):
    print(f"Connexion de {address}")
    
    def receive_messages():
        while True:
            try:
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
                    print(f"Message de {address} : {message}")
            except:
                break

    threading.Thread(target=receive_messages).start()

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 1234))
server_socket.listen()
print("Serveur en attente de connexions...")

try:
    while True:
        conn, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, address)).start()
except KeyboardInterrupt:
    print("Serveur arrêté.")
finally:
    server_socket.close()
