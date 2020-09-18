import sys
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow, 
QWidget, QDoubleSpinBox, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton,
QPlainTextEdit, QSpinBox)


def create_hint(string):
        """
        Standart hint for user 
        """
        hint = QLabel(string)
        hint.setMaximumHeight(26)
        hint.setFrameStyle(0)
        return hint

class ResultWindow(QWidget):
    """
    Window for results of a computations displaying
    """
    def __init__(self, result=None, message="", add_v=False):
        super().__init__()

        self.setWindowTitle("Результати")

        self.main_layout = QVBoxLayout()
        hint = create_hint(message)
        self.main_layout.addWidget(hint)
        
        if result is not None:
            self.layout = QGridLayout()

            if callable(result):
                self.compute_res = result
                result = result()
                self.m = len(result)
            
            for i in range(len(result)):
                self.layout.addWidget(QLabel(str(result[i])), i, 0)
                if callable(self.compute_res):
                    spin_box = QDoubleSpinBox()
                    spin_box.setMinimum(-99.99)
                    self.layout.addWidget(spin_box, i, 2)

            matrix_display = QWidget()
            matrix_display.setLayout(self.layout)
            self.main_layout.addWidget(matrix_display)

            if callable(self.compute_res):
                button_compute = QPushButton()
                button_compute.setText("Ввести вектор v")
                button_compute.clicked.connect(self.compute_with_v)
                self.main_layout.addWidget(button_compute)

        self.setLayout(self.main_layout)
    
    def compute_with_v(self):
        data = np.zeros((self.m,1))
        for i in range(self.m):
            item = self.layout.itemAtPosition(i, 2).widget()
            data[i, 0] = float(item.cleanText().replace(',','.'))
        
        res = self.compute_res(data)
        for i in range(self.m):
            item = self.layout.itemAtPosition(i, 0).widget()
            item.setText(str(res[i][0]))

    


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.is_added = False

        self.main_layout = QVBoxLayout()
        first_input = QHBoxLayout()
        
        hint = create_hint("Введіть m та n:")
        self.main_layout.addWidget(hint)

        self.m_input = QSpinBox()
        self.n_input = QSpinBox()

        first_input.addWidget(self.m_input)
        first_input.addWidget(self.n_input)

        self.button_pass_args = QPushButton()
        self.button_pass_args.setText("Ввести")
        self.button_pass_args.clicked.connect(self.the_button_was_clicked)
        
        first_input.addWidget(self.button_pass_args)
        firs_input_widget = QWidget()
        firs_input_widget.setLayout(first_input)
        self.main_layout.addWidget(firs_input_widget)

        main_widget = QWidget()
        main_widget.setLayout(self.main_layout)

        self.setCentralWidget(main_widget)
    
    def the_button_was_clicked(self):
        """ 
        Slot for processing signal from
        first button, that adds input
        matrix and vector of right dimension
        to the main layout.
        """
        if self.is_added:
            self.delete_from_main_layout()
        else:
            self.is_added = True

        self.m, self.n = int(self.m_input.cleanText()), int(self.n_input.cleanText())

        self.matrix, self.matrix_layout = self.create_matrix_input(self.m, self.n)
        self.vector_b, self.vector_layout = self.create_matrix_input(self.m, 1)
        hint = create_hint("Введіть вектор b:")
        
        self.button_compute = QPushButton()
        self.button_compute.setText("Знайти розвязок")
        self.button_compute.clicked.connect(self.compute_result)

        self.main_layout.addWidget(create_hint('Введіть матрицю A:'))
        self.main_layout.addWidget(self.matrix)
        self.main_layout.addWidget(hint)
        self.main_layout.addWidget(self.vector_b)
        self.main_layout.addWidget(self.button_compute)

    def create_matrix_input(self, m, n):
        """
        Creating input matrix of 
        spinBoxes with (m, n) shape
        """

        layout = QGridLayout()

        for i in range(m):
            for j in range(n):
                spin_box = QDoubleSpinBox()
                spin_box.setMinimum(-99.99)
                layout.addWidget(spin_box, i, j)

        widget = QWidget()
        widget.setLayout(layout)
        return widget, layout

    def get_data_from_table(self, layout, m, n):
        data = np.zeros((m,n))
        for i in range(m):
            for j in range(n):
                item = layout.itemAtPosition(i, j).widget()
                data[i, j] = float(item.cleanText().replace(',','.'))
        return data
    
    def compute_result(self):
        matrix = self.get_data_from_table(self.matrix_layout, self.m, self.n)
        vector_b = self.get_data_from_table(self.vector_layout, self.m, 1)
        try:
            res = np.linalg.solve(matrix, vector_b)
            message = "Знайшовся точний розвязок!"
        except:
            try:
                inv_A = np.linalg.pinv(matrix)

                def param_funcion(v=np.zeros((self.n, 1))):
                    return inv_A.dot(vector_b) + v - inv_A.dot(matrix.dot(v))
                
                res = param_funcion
                message = "Не вдалося знайти точний розвязок.Знайшовся приблизний."
            except:
                res = None
                message = "Не вдалося знайти жодного розвязку системи."

        self.display_result(res, message)
        
    def display_result(self, result, message):
        self.result_w = ResultWindow(result=result, message=message)
        self.result_w.show()
    
    def delete_from_main_layout(self):
        """
        Clearing layout from widgets
        after updating m and n
        """
        items = []
        for i in range(2, self.main_layout.count()):
            items.append(self.main_layout.itemAt(i).widget())
        for widget in items:
            widget.hide()
            self.main_layout.removeWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
