import socket
import os
import threading
import subprocess

class ServeurSimple:
    def __init__(self, hote, port):
        # Initialisation du serveur avec l'adresse et le port
        self.hote = hote
        self.port = port
        self.socket_serveur = None
        self.actif = True
        self.occupe = False  # Indique si un programme est en cours d'exécution

    def demarrer_serveur(self):
        try:
            # Création et démarrage du socket serveur
            self.socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_serveur.bind((self.hote, self.port))
            self.socket_serveur.listen(5)
            print(f"Serveur démarré sur {self.hote}:{self.port}")

            while self.actif:
                try:
                    # Attente d'une connexion client
                    socket_client, adresse_client = self.socket_serveur.accept()
                    print(f"Connexion reçue de : {adresse_client}")
                    # Création d'un thread pour gérer le client
                    thread = threading.Thread(target=self.gestion_client, args=(socket_client,))
                    thread.start()
                except:
                    continue
        except KeyboardInterrupt:
            # Arrêt propre du serveur si CTRL + C est pressé
            print("\nArrêt du serveur demandé par l'utilisateur.")
        finally:
            self.arreter_serveur()

    def arreter_serveur(self):
        # Fermeture du serveur
        self.actif = False
        if self.socket_serveur:
            self.socket_serveur.close()
        print("Serveur arrêté.")

    def gestion_client(self, socket_client):
        # Gère un client qui envoie un fichier
        while True:
            if self.occupe:
                socket_client.sendall("Serveur occupé, veuillez réessayer plus tard.\n".encode("utf-8"))
                break
            self.occupe = True  # Marque le serveur comme occupé
            try:
                # Réception du chemin du fichier
                chemin_fichier = socket_client.recv(4096).decode("utf-8").strip()
                if not chemin_fichier:
                    break
                print(f"Fichier reçu : {chemin_fichier}")

                # Calcul du temps avant l'exécution
                debut_execution = os.times()[4]

                # Exécution en fonction du type de fichier
                if chemin_fichier.endswith(".exe"):
                    resultat = self.executer_exe(chemin_fichier)
                elif chemin_fichier.endswith(".py"):
                    resultat = self.executer_python(chemin_fichier)
                elif chemin_fichier.endswith(".c"):
                    resultat = self.executer_c(chemin_fichier)
                elif chemin_fichier.endswith(".cpp"):
                    resultat = self.executer_cpp(chemin_fichier)
                else:
                    resultat = "Erreur : Type de fichier non pris en charge."

                # Calcul du temps après l'exécution
                fin_execution = os.times()[4]
                temps_execution = fin_execution - debut_execution

                # Affichage dans les logs du serveur
                print(f"Temps d'exécution : {temps_execution:.4f} secondes")
                print(f"Résultat : {resultat.strip()}")

                # Envoi du résultat au client
                socket_client.sendall(f"{resultat.strip()}\nTemps d'exécution : {temps_execution:.4f} secondes\n".encode("utf-8"))
            except Exception as e:
                socket_client.sendall(f"Erreur : {e}\n".encode("utf-8"))
            finally:
                self.occupe = False
        socket_client.close()

    def executer_python(self, chemin_fichier):
        # Exécution d'un script Python
        try:
            execution = subprocess.run(["python", chemin_fichier], capture_output=True, text=True)
            return execution.stdout if execution.returncode == 0 else f"Erreur lors de l'exécution :\n{execution.stderr}"
        except Exception as e:
            return f"Erreur lors de l'exécution du code Python : {e}"

    def executer_exe(self, chemin_fichier):
        # Exécution d'un fichier .exe
        try:
            execution = subprocess.run([chemin_fichier], capture_output=True, text=True)
            return execution.stdout if execution.returncode == 0 else f"Erreur lors de l'exécution :\n{execution.stderr}"
        except Exception as e:
            return f"Erreur lors de l'exécution du fichier .exe : {e}"

    def executer_c(self, chemin_fichier):
        # Compilation et exécution d'un fichier C
        try:
            fichier_exe = "temp_programme.exe"
            compilation = subprocess.run(["gcc", chemin_fichier, "-o", fichier_exe], capture_output=True, text=True)
            if compilation.returncode != 0:
                return f"Erreur de compilation C :\n{compilation.stderr}"
            execution = subprocess.run([fichier_exe], capture_output=True, text=True)
            os.remove(fichier_exe)
            return execution.stdout if execution.returncode == 0 else f"Erreur lors de l'exécution :\n{execution.stderr}"
        except Exception as e:
            return f"Erreur lors de l'exécution du code C : {e}"

    def executer_cpp(self, chemin_fichier):
        # Compilation et exécution d'un fichier C++
        try:
            fichier_exe = "temp_programme_cpp.exe"
            compilation = subprocess.run(["g++", chemin_fichier, "-o", fichier_exe], capture_output=True, text=True)
            if compilation.returncode != 0:
                return f"Erreur de compilation C++ :\n{compilation.stderr}"
            execution = subprocess.run([fichier_exe], capture_output=True, text=True)
            os.remove(fichier_exe)
            return execution.stdout if execution.returncode == 0 else f"Erreur lors de l'exécution :\n{execution.stderr}"
        except Exception as e:
            return f"Erreur lors de l'exécution du code C++ : {e}"

def charger_config():
    # Chargement de la configuration à partir du fichier config.txt
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
        return "localhost", 4000

if __name__ == "__main__":
    # Lancement du serveur
    hote, port = charger_config()
    serveur = ServeurSimple(hote, port)
    serveur.demarrer_serveur()
