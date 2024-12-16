import socket
import os
import threading

class SimpleServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = True
        self.busy = False

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Serveur démarré sur {self.host}:{self.port}")
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Connexion reçue de : {client_address}")
                    thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                    thread.start()
                except KeyboardInterrupt:
                    print("\nArrêt du serveur demandé par l'utilisateur.")
                    break
        except KeyboardInterrupt:
            print("\nArrêt du serveur demandé par l'utilisateur.")
        finally:
            self.stop_server()

    def stop_server(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Serveur arrêté.")

    def handle_client(self, client_socket):
        if self.busy:
            client_socket.sendall("Serveur occupé, connectez-vous à un autre serveur.\n".encode("utf-8"))
            client_socket.close()
            return
        self.busy = True
        try:
            data = client_socket.recv(4096).decode("utf-8")
            if not data:
                return
            print("Code reçu :", data)
            result = self.execute_code(data)
            client_socket.sendall(result.encode("utf-8"))
        except Exception as e:
            client_socket.sendall(f"Erreur : {e}".encode("utf-8"))
        finally:
            self.busy = False
            client_socket.close()

    def execute_code(self, code):
        temp_file = "temp_program.py"
        file = open(temp_file, "w")
        file.write(code)
        file.close()
        result = os.popen(f"python {temp_file}").read()
        os.remove(temp_file)
        return result

def load_config():
    try:
        file = open("config.txt", "r")
        lines = file.readlines()
        file.close()
        host = "localhost"
        port = 4000
        for line in lines:
            if "host=" in line:
                host = line.split("=")[1].strip()
            elif "port=" in line:
                port = int(line.split("=")[1].strip())
        return host, port
    except:
        return "localhost", 4000

if __name__ == "__main__":
    host, port = load_config()
    server = SimpleServer(host, port)
    server.start_server()
