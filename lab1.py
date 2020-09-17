import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton  # <1>


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # <2>

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)

        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        self.setCentralWidget(button)  # <3>
    
    def the_button_was_clicked(self):
        print("Clicked!")
    
    def the_button_was_toggled(self, checked):
        print("Checked?", checked)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
