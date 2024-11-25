import sys
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        lab = QLabel("Saisir votre nom")
        self.message = QLabel("")
        self.text = QLineEdit("")
        ok = QPushButton("Ok")
        quit = QPushButton("Quitter")
        # Ajouter les composants au grid ayout
        grid.addWidget(self.message, 1, 1)
        grid.addWidget(self.text, 2, 2)
        grid.addWidget(lab, 0, 0)
        grid.addWidget(ok, 3, 2)
        grid.addWidget(quit, 2, 0)
        ok.clicked.connect(self.__actionOk)
        quit.clicked.connect(self.__actionQuitter)

        self.setWindowTitle("Une première fenêtre")
    def __actionOk(self):
        prenom = self.text.text()
        if prenom.strip():
            self.message.setText(f"Bonjour {prenom}")
        else:
            self.message.setText("Veuillez entrez un prénom")

    def __actionQuitter(self):
        QCoreApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()