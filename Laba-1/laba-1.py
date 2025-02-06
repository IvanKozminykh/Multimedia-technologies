import sys
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QGraphicsScene, QGraphicsView


# Определение функций
def f1(x):
    return np.sin(x)


def f2(x):
    return np.cos(x)


def f3(x):
    return x ** 2


# Список функций
functions = [f1, f2, f3]


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графики функций")

        # Инициализация элементов интерфейса
        self.layout = QVBoxLayout()

        self.input_layout = QHBoxLayout()

        self.function_count_label = QLabel("Количество функций (1-3):")
        self.function_count_input = QLineEdit()

        self.function_numbers_label = QLabel("Номера функций (через запятую):")
        self.function_numbers_input = QLineEdit()

        self.interval_label = QLabel("Интервал (начало, конец):")
        self.interval_input = QLineEdit()

        self.grid_step_label = QLabel("Шаг сетки:")
        self.grid_step_input = QLineEdit()

        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_graph)

        self.input_layout.addWidget(self.function_count_label)
        self.input_layout.addWidget(self.function_count_input)
        self.input_layout.addWidget(self.function_numbers_label)
        self.input_layout.addWidget(self.function_numbers_input)
        self.input_layout.addWidget(self.interval_label)
        self.input_layout.addWidget(self.interval_input)
        self.input_layout.addWidget(self.grid_step_label)
        self.input_layout.addWidget(self.grid_step_input)
        self.input_layout.addWidget(self.plot_button)

        self.layout.addLayout(self.input_layout)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)

    def plot_graph(self):
        # Получение введенных данных
        try:
            function_count = int(self.function_count_input.text())
            function_numbers = list(map(int, self.function_numbers_input.text().split(',')))
            start, end = map(float, self.interval_input.text().split(','))
            grid_step = float(self.grid_step_input.text())

            if function_count < 1 or function_count > 3 or len(function_numbers) != function_count:
                raise ValueError("Неверное количество функций или номеров функций")

            if not (start < end):
                raise ValueError("Неверный интервал")

            if grid_step <= 0:
                raise ValueError("Шаг сетки должен быть положительным")

            # Очищаем предыдущий график
            self.scene.clear()

            # Устанавливаем белый фон для сцены
            self.scene.setBackgroundBrush(QColor(255, 255, 255))

            # Рисуем сетку
            self.draw_grid(start, end, grid_step)

            # Подготовка данных для графиков
            x = np.linspace(start, end, 500)
            colors = [Qt.red, Qt.green, Qt.blue]

            for i, func_num in enumerate(function_numbers):
                func = functions[func_num - 1]
                y = func(x)

                # Рисуем график
                self.draw_graph(x, y, colors[i])

        except Exception as e:
            print(f"Ошибка: {e}")

    def draw_graph(self, x, y, color):
        # Рисование графика на scene
        pen = QPen(QColor(color))
        pen.setWidth(2)

        for i in range(1, len(x)):
            self.scene.addLine(x[i - 1] * 50 + 250, -y[i - 1] * 50 + 250, x[i] * 50 + 250, -y[i] * 50 + 250, pen)

    def draw_grid(self, start, end, step):
        # Настройки для сетки
        grid_color = QColor(200, 200, 200)  # Светло-серый цвет сетки
        grid_pen = QPen(grid_color)

        # Рисуем вертикальные линии сетки (по оси X)
        for i in np.arange(start, end + step, step):
            self.scene.addLine(i * 50 + 250, -250, i * 50 + 250, 500, grid_pen)

        # Рисуем горизонтальные линии сетки (по оси Y)
        for i in np.arange(-max(abs(start), abs(end)), max(abs(start), abs(end)) + step, step):
            self.scene.addLine(-250, i * 50 + 250, 500, i * 50 + 250, grid_pen)

        # Подписи по оси X (снизу)
        font = QFont()
        font.setPointSize(10)

        # Рисуем подписи по оси X
        for i in np.arange(start, end + step, step):
            text_item = self.scene.addText(str(round(i, 2)), font)
            text_item.setPos(i * 50 + 240, 520)
            text_item.setDefaultTextColor(QColor(0, 0, 0))

        # Подписи по оси Y (справа)
        for i in np.arange(-max(abs(start), abs(end)), max(abs(start), abs(end)) + step, step):
            text_item = self.scene.addText(str(round(i, 2)), font)
            text_item.setPos(530, i * 50 + 240)
            text_item.setDefaultTextColor(QColor(0, 0, 0))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GraphWidget()
    window.resize(600, 600)
    window.show()

    sys.exit(app.exec())
