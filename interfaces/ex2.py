import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversion de Température")
        self.setFixedSize(400, 200)

        widget = QWidget()
        self.setCentralWidget(widget)

        grid = QGridLayout()
        widget.setLayout(grid)

        self.label_temp = QLabel("Température :")
        self.input_temp = QLineEdit()


        self.unit_label = QLabel("°C")
        self.combo_units = QComboBox()
        self.combo_units.addItems(["°C -> K", "K -> °C"])

        self.convert_button = QPushButton("Convertir")

        self.result_label = QLabel("Conversion :")
        self.result_display = QLineEdit()
        self.result_display.setEnabled(False)
        self.result_unit_label = QLabel("K")

        self.help_button = QPushButton("?")
        self.help_button.setFixedSize(30, 30)

        grid.addWidget(self.label_temp, 0, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.input_temp, 0, 1)
        grid.addWidget(self.unit_label, 0, 2)

        grid.addWidget(self.convert_button, 1, 1)

        grid.addWidget(self.combo_units, 1, 2)

        grid.addWidget(self.result_label, 2, 0, alignment=Qt.AlignRight)
        grid.addWidget(self.result_display, 2, 1)
        grid.addWidget(self.result_unit_label, 2, 2)

        grid.addWidget(self.help_button, 3, 2, alignment=Qt.AlignRight)

        self.convert_button.clicked.connect(self.__convert_temperature)
        self.combo_units.currentIndexChanged.connect(self.__update_units)
        self.help_button.clicked.connect(self.__show_help)

    def __convert_temperature(self):
        try:
            temp = float(self.input_temp.text())
            selected_conversion = self.combo_units.currentText()

            if selected_conversion == "°C -> K":
                if temp < -273.15:
                    raise ValueError("Température inférieure au zéro absolu en Celsius.")
                result = temp + 273.15
                self.result_unit_label.setText("K")
            elif selected_conversion == "K -> °C":
                if temp < 0:
                    raise ValueError("Température inférieure au zéro absolu en Kelvin.")
                result = temp - 273.15
                self.result_unit_label.setText("°C")

            self.result_display.setText(f"{result:.2f}")
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))
        except Exception:
            QMessageBox.critical(self, "Erreur", "Saisie invalide. Veuillez entrer un nombre.")

    def __update_units(self):
        selected_conversion = self.combo_units.currentText()
        if selected_conversion == "°C -> K":
            self.unit_label.setText("°C")
            self.result_unit_label.setText("K")
        elif selected_conversion == "K -> °C":
            self.unit_label.setText("K")
            self.result_unit_label.setText("°C")

    def __show_help(self):
        QMessageBox.information(
            self,
            "Aide",
            "Permet de convertir un nombre soit de Kelvin vers Celsius, soit de Celsius vers Kelvin.\n\n"
            "• Kelvin → Celsius : soustraction de 273.15.\n"
            "• Celsius → Kelvin : addition de 273.15.\n"
            "• Attention : une température ne peut pas être inférieure au zéro absolu (-273.15 °C ou 0 K)."
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
