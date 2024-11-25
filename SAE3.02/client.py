import sys
import socket
from PyQt6.QtWidgets import *

class ClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client de Compilation - PyQt6")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Adresse IP
        self.ip_label = QLabel("Adresse IP du Serveur :")
        layout.addWidget(self.ip_label)
        self.ip_entry = QLineEdit("127.0.0.1")
        layout.addWidget(self.ip_entry)

        # Port
        self.port_label = QLabel("Port du Serveur :")
        layout.addWidget(self.port_label)
        self.port_entry = QLineEdit("12345")
        layout.addWidget(self.port_entry)

        # Bouton pour choisir le fichier
        self.file_button = QPushButton("Choisir un fichier")
        self.file_button.clicked.connect(self.choose_file)
        layout.addWidget(self.file_button)

        # Affichage du chemin du fichier
        self.file_path_label = QLabel("Aucun fichier sélectionné")
        layout.addWidget(self.file_path_label)

        # Bouton pour envoyer le programme
        self.send_button = QPushButton("Envoyer le Programme")
        self.send_button.clicked.connect(self.send_program)
        layout.addWidget(self.send_button)

        # Zone de texte pour afficher le résultat
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier Python", "", "Python Files (*.py)")
        if file_path:
            self.file_path_label.setText(file_path)
            self.file_path = file_path

    def send_program(self):
        ip = self.ip_entry.text()
        port = int(self.port_entry.text())

        if not hasattr(self, 'file_path'):
            self.output_text.setText("Veuillez sélectionner un fichier avant d'envoyer.")
            return

        try:
            with open(self.file_path, "r") as file:
                program = file.read()

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            client_socket.sendall(program.encode('utf-8'))

            result = client_socket.recv(4096).decode('utf-8')
            self.output_text.setText(result)
        except Exception as e:
            self.output_text.setText(f"Erreur : {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_app = ClientApp()
    client_app.show()
    sys.exit(app.exec())
