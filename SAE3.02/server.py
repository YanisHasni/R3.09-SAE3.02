import socket
import threading
import os
import subprocess

def handle_client(client_socket):
    try:
        # Recevoir le programme
        program = client_socket.recv(4096).decode('utf-8')
        if not program:
            return

        # Écrire le programme dans un fichier temporaire
        with open("temp_program.py", "w") as file:
            file.write(program)

        # Exécuter le programme
        result = subprocess.run(["python", "temp_program.py"], capture_output=True, text=True)
        output = result.stdout + result.stderr

        # Envoyer le résultat au client
        client_socket.sendall(output.encode('utf-8'))
    finally:
        client_socket.close()
        # Supprimer le fichier temporaire
        os.remove("temp_program.py")

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"Serveur démarré sur le port {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connexion de {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server(12345)
