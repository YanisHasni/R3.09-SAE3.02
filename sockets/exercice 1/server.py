import socket;

server_socket = socket.socket()
server_socket.bind(('127.0.0.1', 1235))
server_socket.listen(1)
conn, address = server_socket.accept()
print("Connexion du client au serveur")
message = conn.recv(1024).decode()
reply = "Message Reçu"
conn.send(reply.encode())
print("Client : " , message)
conn.close()
server_socket.close()