import math
import sys

import matplotlib
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('QT5Agg')


class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        fig = FigureCanvas(Figure(figsize=(width, height), dpi=dpi))
        self.axes = fig.figure.add_subplot(111)
        self.axes.grid(True)
        super().__init__(fig.figure)


def get_solution_linear_equation(c, d):
    return - float(d)/float(c)


def get_solution_quad_equation(a, b, c):
    a = float(a)
    b = float(b)
    c = float(c)
    if not math.isclose(a, 0.):
        discreminant = b**2 - 4*a*c
        if math.isclose(discreminant, 0.):
            return - b / (2*a), - b / (2*a)
        elif discreminant < 0.:
            return None, None
        else:
            return (- b + math.sqrt(discreminant))/(2*a), (- b - math.sqrt(discreminant))/(2*a)
    else:
        return get_solution_linear_equation(b, c), None


def y(a, b, c, d, x):
    return float(a)*(x**3) + float(b)*(x**2) + float(c)*x + float(d)


def get_solution_third_equation(a, b, c, d, right, left):
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    right = float(right)
    left = float(left)
    left_local = left
    right_local = right

    while True:
        x = (left_local + right_local) / 2.
        if math.isclose(y(a, b, c, d, x)+1., 1.):
            result1 = x
            break
        elif (y(a, b, c, d, x) > 0.) & (y(a, b, c, d, left_local) > 0.):
            left_local = x
        elif (y(a, b, c, d, x) > 0.) & (y(a, b, c, d, right_local) > 0.):
            right_local = x
        elif (y(a, b, c, d, x) < 0.) & (y(a, b, c, d, left_local) < 0.):
            left_local = x
        elif (y(a, b, c, d, x) < 0.) & (y(a, b, c, d, right_local) < 0.):
            right_local = x
    result2, result3 = get_solution_quad_equation(a, (b + a*result1), (c + (b * result1) + (a * result1 * result1)))
    return result1, result2, result3


# Создаем класс  главного окна, на котором распологаются все поля и график
# Класс наследуется от класса QMainWindow
class MainWindow(QMainWindow):
    # объявляем метод init - он срабатывает при инициализации окна и отрисовки всей графики
    def __init__(self):
        # вызываем родительский метод init
        super().__init__()
        # указываем название окна Решатель кубов
        self.setWindowTitle("Решатель кубов")

        # Устанавливааем центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # На центральном виджете устанавливаем слой с полями и графиком
        self.layout = QVBoxLayout(self.central_widget)
        # задаем поле А и подпись к нему
        self.labelA = QLabel("A:")
        self.inputA = QLineEdit()
        # задаем поле B и подпись к нему
        self.labelB = QLabel("B:")
        self.inputB = QLineEdit()
        # задаем поле C и подпись к нему
        self.labelC = QLabel("C:")
        self.inputC = QLineEdit()
        # задаем поле D и подпись к нему
        self.labelD = QLabel("D:")
        self.inputD = QLineEdit()
        # задаем поле X от и подпись к нему
        self.label_left_border = QLabel("X от:")
        self.input_left_border = QLineEdit()
        # задаем поле до и подпись к нему
        self.label_right_border = QLabel("до:")
        self.input_right_border = QLineEdit()

        # Задаем главную надпись A*X^3 + B*x^2 + C*x + D = 0
        self.label = QLabel("A*X^3 + B*x^2 + C*x + D = 0")
        # устанавливаем главную надпись на слой на главном виджете A*X^3 + B*x^2 + C*x + D = 0
        self.layout.addWidget(self.label)
        # устанавливаем поле для ввода А и надпись к полю
        self.layout.addWidget(self.labelA)
        self.layout.addWidget(self.inputA)
        # устанавливаем поле для ввода В и надпись к полю
        self.layout.addWidget(self.labelB)
        self.layout.addWidget(self.inputB)
        # устанавливаем поле для ввода C и надпись к полю
        self.layout.addWidget(self.labelC)
        self.layout.addWidget(self.inputC)
        # устанавливаем поле для ввода D и надпись к полю
        self.layout.addWidget(self.labelD)
        self.layout.addWidget(self.inputD)
        # устанавливаем поле для ввода 'от' и надпись к полю
        self.layout.addWidget(self.label_left_border)
        self.layout.addWidget(self.input_left_border)
        # устанавливаем поле для ввода 'до' и надпись к полю
        self.layout.addWidget(self.label_right_border)
        self.layout.addWidget(self.input_right_border)
        # Объявляем кнопку Построить график и устанавливаем ее на слой
        self.button = QPushButton("Построить график")
        self.layout.addWidget(self.button)

        # Объявляем кнопку Найти решение и устанавливаем ее на слой
        self.button_find_solution = QPushButton("Найти решение")
        self.layout.addWidget(self.button_find_solution)

        # Добавляем пустое место на слой для вывода корней
        self.label_result1 = QLabel("")
        self.layout.addWidget(self.label_result1)
        self.label_result2 = QLabel("")
        self.layout.addWidget(self.label_result2)
        self.label_result3 = QLabel("")
        self.layout.addWidget(self.label_result3)

        # Указываем что при нажатии кнопки построить график будет вызываться функция on_button_clicked
        self.button.clicked.connect(self.on_button_clicked)
        # Указываем что при нажатии кнопки найти решение будет вызываться функция on_button_find_solution_clicked
        self.button_find_solution.clicked.connect(self.on_button_find_solution_clicked)

        # Добавляем график на слой
        self.canvas = MplCanvas(width=6, height=10, dpi=100)
        self.layout.addWidget(self.canvas)

    # функция, чтобы получить все данные А, B, C, D, от и до с окна
    def get_data(self):
        a = self.inputA.text()
        b = self.inputB.text()
        c = self.inputC.text()
        d = self.inputD.text()
        right_border = self.input_right_border.text()
        left_border = self.input_left_border.text()

        if a == '':
            a = '0'
            self.inputA.setText('0')
        if b == '':
            b = '0'
            self.inputB.setText('0')
        if c == '':
            c = '0'
            self.inputC.setText('0')
        if d == '':
            d = '0'
            self.inputD.setText('0')

        if right_border == '':
            right_border = '10'
            self.input_right_border.setText('10')
        if left_border == '':
            left_border = '-10'
            self.input_left_border.setText('-10')
        return a, b, c, d, left_border, right_border

    def on_button_clicked(self):
        a, b, c, d, left_border, right_border = self.get_data()
        x = np.linspace(float(left_border), float(right_border), 1000)
        result = []
        for item in x:
            result.append(y(a, b, c, d, item))
        self.layout.removeWidget(self.canvas)
        self.canvas = MplCanvas(width=6, height=10, dpi=100)
        self.canvas.axes.plot(x, result)

        self.canvas.draw_idle()
        self.layout.addWidget(self.canvas)

    def on_button_find_solution_clicked(self):
        self.label_result1.setText('')
        self.label_result2.setText('')
        self.label_result3.setText('')
        a, b, c, d, left_border, right_border = self.get_data()

        if (a == '0') & (b == '0') & (c == '0') & (d == '0'):
            self.label_result1.setText('Не задано уравнение!')
        elif (a == '0') & (b == '0') & (c == '0') & (d != '0'):
            self.label_result1.setText('Не возможно решить!')
        elif (a == '0') & (b == '0') & (c != '0'):
            x1 = get_solution_linear_equation(c, d)
            self.label_result1.setText(f'x1:={x1:.8f}')
        elif (a == '0') & (b != '0'):
            x1, x2 = get_solution_quad_equation(b, c, d)
            if x1 is not None:
                self.label_result1.setText(f'x1:={x1:.8f}')
            if x2 is not None:
                self.label_result2.setText(f'x2:={x2:.8f}')
        elif a != '0':

            x1, x2, x3 = get_solution_third_equation(a, b, c, d, right_border, left_border)
            if x1 is not None:
                self.label_result1.setText(f'x1:={x1:.8f}')
            if x2 is not None:
                self.label_result2.setText(f'x2:={x2:.8f}')
            if x3 is not None:
                self.label_result3.setText(f'x3:={x3:.8f}')


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
