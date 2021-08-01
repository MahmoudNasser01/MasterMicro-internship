# Pyside2 GUI libraries
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, \
    QDoubleSpinBox, QMessageBox, QStatusBar
from PySide2.QtGui import QPixmap, QPalette, QColor
from PySide2.QtCore import QSize, Qt
# Plotter libraries
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
# Processing libraries
import numpy as np
import sys
import re
from formatter import input_formatted_to_func
import styles

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(900, 700))

        # error message holder
        self.error = ""

        # Input Layout Components
        self.input_layout = QHBoxLayout()
        self.function_input = QLineEdit("")
        self.button_to_conv = QPushButton("Plot")
        self.input_layout.setAlignment(Qt.AlignTop)
        self.input_layout.addWidget(self.button_to_conv)
        self.input_layout.addWidget(self.function_input)

        # Range Layout Components
        self.range_layout = QHBoxLayout()
        self.min_input = QDoubleSpinBox()
        self.min_input.setPrefix("Min value: ")
        self.min_input.setRange(-3000, 3000)
        self.min_input.setValue(-10)
        self.max_input = QDoubleSpinBox()
        self.max_input.setPrefix("Max value: ")
        self.max_input.setRange(-3000, 3000)
        self.max_input.setValue(10)
        self.range_layout.setAlignment(Qt.AlignTop)
        self.range_layout.addWidget(self.min_input)
        self.range_layout.addWidget(self.max_input)

        # Matplotlib figure (Plot)
        self.canvas = FigureCanvas(Figure(figsize=(8, 8)))
        self.ax = self.canvas.figure.subplots()
        self.ax.set_xlabel("X-Axis")
        self.ax.set_ylabel("Y-Axis")
        self.ax.grid()

        # Main Layout Grouper
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.canvas)
        self.main_layout.addLayout(self.range_layout)

        # Error Message Box Layout
        self.err_msg = QMessageBox()
        self.err_msg.setStyleSheet("QLabel{color:red}")



        # Other properties will be adjusted depending on \
        # the error type.
        # Logic Wrapper

        """
            Note: lambada function is used for re invoke the plot function once any update happend
        """

        self.button_to_conv.clicked.connect(lambda _: self.plotter(None))

        self.min_input.valueChanged.connect(lambda _: self.plotter("min"))

        self.max_input.valueChanged.connect(lambda _: self.plotter("max"))

        # Load main layout
        self.setLayout(self.main_layout)


        # Styling the app
        self.setStyleSheet(styles.app_style)
        self.function_input.setStyleSheet(styles.input_field_style)
        self.button_to_conv.setStyleSheet(styles.plot_button_style)
        self.min_input.setStyleSheet(styles.min_button_style)
        self.max_input.setStyleSheet(styles.max_button_style)


    # here we impl the main function of the process
    def plotter(self, event):

        min_val = self.min_input.value()
        max_val = self.max_input.value()

        # Validate Range
        if min_val >= max_val and event == "min":
            self.err_msg.setWindowTitle("Range Error!")
            self.err_msg.setText("Minimum input must be less than Maximum input")
            self.err_msg.show()
            self.min_input.setValue(max_val - 1)
        elif max_val <= min_val and event == "max":
            self.err_msg.setWindowTitle("Range Error!")
            self.err_msg.setText("Maximum input must be bigger than Minimum input")
            self.err_msg.show()
            self.max_input.setValue(min_val + 1)
        else:
            # Create required range
            x = np.linspace(min_val, max_val)
            try:
                y = input_formatted_to_func(self.function_input.text())(x)
            except ValueError as err:
                self.err_msg.setWindowTitle("Function Error!")
                self.err_msg.setText(str(err))
                self.error = self.err_msg.text()
                self.err_msg.show()
                return

            self.error = self.err_msg.text()

            print(self.error)
            # Update plot
            self.ax.clear()

            self.ax.plot(x, y)
            self.ax.grid()
            self.canvas.draw()


# project werpper
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())
