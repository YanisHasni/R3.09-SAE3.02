import socket
import os
import sys
from PyQt6.QtWidgets import *

class ApplicationClient(QMainWindow):
    def __init__(self):
        super().__init__()
        # Configuration de la fenêtre principale
        self.setWindowTitle("Client - Envoi de programme")
        self.setGeometry(100, 100, 500, 400)
        self.hote_serveur, self.port_serveur = self.charger_config()  # Charger l'hôte et le port depuis config.txt
        self.fichier_selectionne = None
        self.socket_client = None

        # Création des widgets de l'interface
        layout = QVBoxLayout()

        self.etiquette_hote = QLabel(f"Hôte du serveur : {self.hote_serveur}")
        layout.addWidget(self.etiquette_hote)

        self.etiquette_port = QLabel(f"Port du serveur : {self.port_serveur}")
        layout.addWidget(self.etiquette_port)

        self.bouton_connexion = QPushButton("Se connecter au serveur")
        self.bouton_connexion.clicked.connect(self.se_connecter_au_serveur)  # Bouton pour se connecter au serveur
        layout.addWidget(self.bouton_connexion)

        self.bouton_selectionner_fichier = QPushButton("Sélectionner un fichier")
        self.bouton_selectionner_fichier.clicked.connect(self.selectionner_fichier)  # Bouton pour choisir un fichier
        self.bouton_selectionner_fichier.setEnabled(False)  # Désactivé tant que le client n'est pas connecté
        layout.addWidget(self.bouton_selectionner_fichier)

        self.etiquette_fichier = QLabel("Aucun fichier sélectionné.")
        layout.addWidget(self.etiquette_fichier)

        self.bouton_envoyer = QPushButton("Envoyer au serveur")
        self.bouton_envoyer.clicked.connect(self.envoyer_programme)  # Bouton pour envoyer le fichier
        self.bouton_envoyer.setEnabled(False)  # Désactivé tant qu'aucun fichier n'est sélectionné
        layout.addWidget(self.bouton_envoyer)

        self.affichage_resultat = QTextEdit()  # Zone de texte pour afficher les résultats
        self.affichage_resultat.setReadOnly(True)
        layout.addWidget(self.affichage_resultat)

        # Ajouter les widgets dans la fenêtre principale
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def charger_config(self):
        # Charger l'hôte et le port du serveur à partir du fichier config.txt
        try:
            with open("config.txt", "r") as fichier:
                lignes = fichier.readlines()
                hote = "localhost"
                port = 4000
                for ligne in lignes:
                    if "host=" in ligne:
                        hote = ligne.split("=")[1].strip()
                    elif "port=" in ligne:
                        port = int(ligne.split("=")[1].strip())
                return hote, port
        except:
            return "localhost", 4000  # Valeurs par défaut si le fichier config est manquant

    def se_connecter_au_serveur(self):
        # Connexion au serveur
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.connect((self.hote_serveur, self.port_serveur))
            self.affichage_resultat.append("Connecté au serveur.")  # Afficher un message si connecté
            self.bouton_selectionner_fichier.setEnabled(True)  # Activer le bouton pour sélectionner un fichier
            self.bouton_envoyer.setEnabled(True)  # Activer le bouton pour envoyer le fichier
        except Exception as e:
            self.affichage_resultat.append(f"Erreur de connexion : {e}")  # Message en cas d'erreur

    def selectionner_fichier(self):
        # Sélectionner un fichier Python, C ou C++
        chemin_fichier, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier",
            "",
            "Python Files (*.py);;C Files (*.c);;C++ Files (*.cpp)"
        )
        if chemin_fichier:
            self.fichier_selectionne = chemin_fichier
            self.etiquette_fichier.setText(f"Fichier sélectionné : {chemin_fichier}")  # Afficher le chemin
        else:
            self.etiquette_fichier.setText("Aucun fichier sélectionné.")  # Message si aucun fichier n'est choisi

    def envoyer_programme(self):
        # Envoyer le programme au serveur
        if not self.fichier_selectionne:
            self.affichage_resultat.append("Erreur : Aucun fichier sélectionné.")  # Vérifier qu'un fichier est sélectionné
            return
        if not self.socket_client:
            self.affichage_resultat.append("Erreur : Vous n'êtes pas connecté au serveur.")  # Vérifier la connexion
            return
        try:
            # Envoyer le chemin du fichier au serveur
            self.socket_client.sendall(self.fichier_selectionne.encode("utf-8"))
            self.affichage_resultat.append("Envoi du programme au serveur...")

            # Recevoir la réponse du serveur
            reponse = ""
            while True:
                morceau = self.socket_client.recv(4096).decode("utf-8")
                reponse += morceau
                if "\n" in morceau or not morceau:
                    break

            self.affichage_resultat.append(f"Réponse du serveur :\n{reponse.strip()}")  # Afficher la réponse du serveur
        except Exception as e:
            self.affichage_resultat.append(f"Erreur : {e}")  # Afficher une erreur si l'envoi échoue

if __name__ == "__main__":
    # Lancer l'application
    application = QApplication(sys.argv)
    fenetre = ApplicationClient()
    fenetre.show()
    sys.exit(application.exec())
