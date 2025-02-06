import sys
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox,
    QLineEdit, QLabel, QHBoxLayout, QCheckBox
)
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt


class FunctionPlotter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_functions = []

    def initUI(self):
        main_layout = QVBoxLayout()
        controls_layout = QVBoxLayout()

        self.function_selectors = []
        self.checkboxes = []
        functions_layout = QHBoxLayout()
        for i in range(3):
            func_box = QVBoxLayout()
            checkbox = QCheckBox(f'Функция {i + 1}')
            combo = QComboBox()
            combo.addItems(["10*sin(x)", "10*sin(2x + exp(|x|))", "10/sin(x)"])
            self.function_selectors.append(combo)
            self.checkboxes.append(checkbox)
            func_box.addWidget(checkbox)
            func_box.addWidget(combo)
            functions_layout.addLayout(func_box)

        controls_layout.addLayout(functions_layout)

        interval_layout = QHBoxLayout()
        self.start_input = QLineEdit("-10")
        self.end_input = QLineEdit("10")
        interval_layout.addWidget(QLabel("Начало:"))
        interval_layout.addWidget(self.start_input)
        interval_layout.addWidget(QLabel("Конец:"))
        interval_layout.addWidget(self.end_input)
        controls_layout.addLayout(interval_layout)

        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_graph)
        controls_layout.addWidget(self.plot_button)

        main_layout.addLayout(controls_layout)

        self.graph_area = QWidget()
        main_layout.addWidget(self.graph_area, 1)

        self.setLayout(main_layout)
        self.setWindowTitle("Графики функций")
        self.setMinimumSize(800, 600)

    def plot_graph(self):
        try:
            x_start = float(self.start_input.text())
            x_end = float(self.end_input.text())

            self.selected_functions.clear()
            functions = [
                lambda x: 10 * np.sin(x),
                lambda x: 10 * np.sin(2 * x + np.exp(np.abs(x))),
                lambda x: np.where(np.sin(x) != 0, 10 / np.sin(x), np.nan)
            ]

            for i in range(3):
                if self.checkboxes[i].isChecked():
                    func_index = self.function_selectors[i].currentIndex()
                    self.selected_functions.append(functions[func_index])

            self.update()
        except ValueError:
            print("Ошибка: Введите корректные числовые значения для интервала.")

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height() - 200
        margin = 50

        qp.fillRect(margin, margin, width - 2 * margin, height - 2 * margin, Qt.white)
        qp.setPen(QPen(Qt.black, 1))
        qp.drawRect(margin, margin, width - 2 * margin, height - 2 * margin)

        step_x = (width - 2 * margin) / 10
        step_y = (height - 2 * margin) / 10

        for i in range(11):
            x_pos = margin + i * step_x
            y_pos = margin + i * step_y
            qp.drawLine(x_pos, margin, x_pos, height + margin)
            qp.drawLine(margin, y_pos, width - margin, y_pos)
            qp.drawText(x_pos - 10, height + margin + 20, f"{i - 5}")
            qp.drawText(margin - 30, y_pos + 5, f"{5 - i}")

        if not self.selected_functions:
            return

        try:
            x_start = float(self.start_input.text())
            x_end = float(self.end_input.text())
            x_vals = np.linspace(x_start, x_end, width - 2 * margin)

            colors = [Qt.blue, Qt.green, Qt.red]

            for idx, func in enumerate(self.selected_functions):
                qp.setPen(QPen(colors[idx], 2))
                y_vals = func(x_vals)
                y_vals = np.interp(y_vals, (np.nanmin(y_vals), np.nanmax(y_vals)), (height - margin, margin))

                for i in range(1, len(x_vals)):
                    if not np.isnan(y_vals[i - 1]) and not np.isnan(y_vals[i]):
                        x1 = int(margin + i - 1)
                        y1 = int(y_vals[i - 1])
                        x2 = int(margin + i)
                        y2 = int(y_vals[i])
                        qp.drawLine(x1, y1, x2, y2)
        except ValueError:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(app.exec())
