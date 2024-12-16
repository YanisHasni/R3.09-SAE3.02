import socket

def send_program_to_server(host, port, code):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.sendall(code.encode("utf-8"))
        response = client_socket.recv(4096).decode("utf-8")
        print("Réponse du serveur :")
        print(response)
        client_socket.close()
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    host = "localhost"
    port = 5000
    code = """print('Hello from the client!')"""
    send_program_to_server(host, port, code)
