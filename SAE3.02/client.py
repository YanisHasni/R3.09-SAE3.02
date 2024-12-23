import socket
import sys
from PyQt6.QtWidgets import *

class ClientApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client - Envoi de programme")
        self.setGeometry(100, 100, 500, 400)
        self.server_host, self.server_port = self.load_config()
        self.selected_file = None
        self.client_socket = None

        layout = QVBoxLayout()
        self.label_host = QLabel("Hôte du serveur : " + self.server_host)
        layout.addWidget(self.label_host)
        self.label_port = QLabel("Port du serveur : " + str(self.server_port))
        layout.addWidget(self.label_port)

        self.button_connect = QPushButton("Se connecter au serveur")
        self.button_connect.clicked.connect(self.connect_to_server)
        layout.addWidget(self.button_connect)

        self.button_select_file = QPushButton("Sélectionner un fichier")
        self.button_select_file.clicked.connect(self.select_file)
        self.button_select_file.setEnabled(False)
        layout.addWidget(self.button_select_file)

        self.label_file = QLabel("Aucun fichier sélectionné.")
        layout.addWidget(self.label_file)

        self.button_send = QPushButton("Envoyer au serveur")
        self.button_send.clicked.connect(self.send_program)
        self.button_send.setEnabled(False)
        layout.addWidget(self.button_send)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_config(self):
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

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_host, self.server_port))
            response = self.client_socket.recv(1024).decode("utf-8").strip()
            if "Serveur occupé" in response:
                self.result_display.append("Serveur occupé, veuillez réessayer plus tard.")
                self.client_socket.close()
                self.client_socket = None
            else:
                self.result_display.append("Connecté au serveur.")
                self.button_select_file.setEnabled(True)
                self.button_send.setEnabled(True)
        except:
            self.result_display.append("Erreur de connexion.")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "Python Files (*.py)")
        if file_path:
            self.selected_file = file_path
            self.label_file.setText("Fichier sélectionné : " + file_path)
        else:
            self.label_file.setText("Aucun fichier sélectionné.")

    def send_program(self):
        if not self.selected_file:
            self.result_display.append("Erreur : Aucun fichier sélectionné.")
            return
        if not self.client_socket:
            self.result_display.append("Erreur : Vous n'êtes pas connecté au serveur.")
            return
        try:
            file = open(self.selected_file, "r")
            program_content = file.read()
            file.close()
            self.client_socket.sendall(program_content.encode("utf-8"))

            response = ""
            while True:
                chunk = self.client_socket.recv(4096).decode("utf-8")
                response += chunk
                if "\n" in chunk or not chunk:
                    break

            self.result_display.append("Réponse du serveur :\n" + response.strip())
        except:
            self.result_display.append("Erreur lors de l'envoi.")
        finally:
            self.client_socket.close()
            self.client_socket = None
            self.result_display.append("Déconnecté du serveur.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec())
