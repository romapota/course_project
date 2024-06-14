from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout, QHBoxLayout, QLineEdit
import PySide6
import sys
import alg_new_oop as alg
n = 3
busy: int
count: int
positions_lst: list
pos_new: list
size: str
check: bool
check_t: bool
time: str
time_t: str
class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.busy = 0
class Chess(QMainWindow):
    global n
    def __init__(self):
        self.date_input = {'size_pole' : 0, 'count_need_put_fugire': 0, 'posistions': 0}
        super().__init__()
        self.setGeometry(0, 0, 700, 600)
        self.labels = [QLabel() for i in range(n**2)]
        self.positions = []
        for i in range(n):
            for j in range(n):
                self.positions.append([i, j])
        #кнопки и виджеты
        self.main_widget = QWidget()
        self.button_solutions = QPushButton('Рассчитать комбинации')
        self.button_clear = QPushButton('Очистить поле')
        self.label_countOfSolutions = QLabel(f'Количество решений: {0}')
        self.input_size_pole = QLineEdit()
        self.input_count_need_put_fugire = QLineEdit()
        self.input_posistions = QLineEdit()

        #css-стили
        self.label_countOfSolutions.setStyleSheet("""max-height: 10px;""")
        self.input_size_pole.setStyleSheet("""max-width: 200px;""")
        self.input_size_pole.setPlaceholderText("Размер поля:")
        self.input_count_need_put_fugire.setStyleSheet("""max-width: 200px;""")
        self.input_count_need_put_fugire.setPlaceholderText("Количество фигур, которое надо расставить")
        self.input_posistions.setStyleSheet("""max-width: 200px;""")
        self.input_posistions.setPlaceholderText('Фигуры на доске: "(0,0) (0,1) ..."')

        #слои
        self.main_layout = QHBoxLayout()
        self.edit_layout = QVBoxLayout()
        self.buttons_layout = QVBoxLayout()
        self.pole_layout = QGridLayout()

        self.pole_layout.setSpacing(5)
        count = 0
        for i in self.labels:
                self.pole_layout.addWidget(i, self.positions[count][0], self.positions[count][1])
                i.setStyleSheet("""background-color: white;""")
                count += 1

        #добавление элементов в слои и виджеты
        self.buttons_layout.addWidget(self.input_size_pole)
        self.buttons_layout.addWidget(self.input_count_need_put_fugire)
        self.buttons_layout.addWidget(self.input_posistions)
        self.buttons_layout.addWidget(self.button_solutions)
        self.buttons_layout.addWidget(self.button_clear)
        self.buttons_layout.addWidget(self.label_countOfSolutions)
        self.main_layout.addLayout(self.pole_layout)
        self.main_layout.addLayout(self.buttons_layout)
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        #подключение кнопок и форм
        self.button_solutions.setCheckable(True)
        self.button_solutions.clicked.connect(self.find_of_solution)
        self.button_clear.setCheckable(True)
        self.button_clear.clicked.connect(self.clear_pole)
        self.input_size_pole.textEdited.connect(self.save_size_pole)
        self.input_count_need_put_fugire.textEdited.connect(self.save_count_need_figure)
        self.input_posistions.textEdited.connect(self.save_positions)

    def find_of_solution(self) -> None:
            size = self.date_input['size_pole']
            count_put = self.date_input['count_need_put_fugire']
            positions = self.date_input['posistions']
            positions_lst = positions.split(' ')
            pos_new = []
            for i in positions_lst:
                time = ''
                for symbol in i:
                    if symbol in ['0','1','2','3','4','5','6','7','8','9']:
                        time += symbol
                        time += ' '
                pos_new.append(time)

            #сохранение данных в файл intput
            with open('input.txt', 'w') as f:
                s = f"{size} {count_put} {len(pos_new)}\n"
                f.write(s)
                for i in pos_new:
                    f.write(i+'\n')
            date = alg.main()
            count_of_solutions = date[1]
            board = date[0]
            self.label_countOfSolutions.setText(f'Количество решений: {count_of_solutions}')
            labels = [QLabel() for i in range(int(size)**2)]
            for i in range(len(labels)):
                if board[i][2] == 1:
                    self.pole_layout.addWidget(labels[i], board[i][0], board[i][1])
                    labels[i].setStyleSheet("""background-color: red""")
                    continue
                if board[i][2] == 2:
                    self.pole_layout.addWidget(labels[i], board[i][0], board[i][1])
                    labels[i].setStyleSheet("""background-color: yellow""")
                else:
                    self.pole_layout.addWidget(labels[i], board[i][0], board[i][1])
                    labels[i].setStyleSheet("""background-color: green""")
    def clear_pole(self) -> None:
        self.label_countOfSolutions.setText(f'Количество решений: 0')

        #изменение цвета поля ввода
        self.input_size_pole.setStyleSheet("""background-color: none; max-width: 200px;""")
        self.input_count_need_put_fugire.setStyleSheet("""background-color: none; max-width: 200px;""")
        self.input_posistions.setStyleSheet("""background-color: none; max-width: 200px;""")

        #очищение полей ввода
        self.input_count_need_put_fugire.clear()
        self.input_size_pole.clear()
        self.input_posistions.clear()
        size = self.date_input['size_pole']
        #очищение поля
        self.labels = [QLabel() for i in range(int(size) ** 2)]
        self.positions = []
        for i in range(int(size)):
            for j in range(int(size)):
                self.positions.append([i, j])
        count = 0
        for i in self.labels:
                self.pole_layout.addWidget(i, self.positions[count][0], self.positions[count][1])
                i.setStyleSheet("""background-color: white;""")
                count += 1
    def save_size_pole(self, text: str) -> None:
        if self.date_input['size_pole'] != text:
            self.date_input['size_pole'] = text
        for symbol in text:
            if symbol not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.input_size_pole.setStyleSheet("""background-color: #E52B50; max-width: 200px;""")
                self.button_solutions.setEnabled(False)
                break
            else:
                self.input_size_pole.setStyleSheet("""background-color: #26E33B;max-width: 200px;""")
                self.button_solutions.setEnabled(True)
        if text == '':
            self.input_size_pole.setStyleSheet("""background-color: none; max-width: 200px;""")
            self.button_solutions.setEnabled(True)
    def save_count_need_figure(self, text: str) -> None:
        if self.date_input['count_need_put_fugire'] != text:
            self.date_input['count_need_put_fugire'] = text
        for symbol in text:
            if symbol not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.input_count_need_put_fugire.setStyleSheet("""background-color: #E52B50; max-width: 200px;""")
                self.button_solutions.setEnabled(False)
                break
            else:
                self.input_count_need_put_fugire.setStyleSheet("""background-color: #26E33B; max-width: 200px;""")
                self.button_solutions.setEnabled(True)
        if text == '':
            self.input_count_need_put_fugire.setStyleSheet("""background-color: none; max-width: 200px;""")
            self.button_solutions.setEnabled(True)
    def save_positions(self, text: str) -> None:
        check = False
        check_t = False
        if self.date_input['posistions'] != text:
            self.date_input['posistions'] = text
        time = ''
        time_t = ''
        for symbol in text:
            if symbol not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', ',', ' ']:
                self.input_posistions.setStyleSheet("""background-color: #E52B50; max-width: 200px;""")
                self.button_solutions.setEnabled(False)
                break
            if check:
                time += symbol
            if symbol == '(':
                check = True
                time += symbol
            if symbol == ')' and check:
                check = False
                if ' ' in time:
                    self.input_posistions.setStyleSheet("""background-color: #E52B50; max-width: 200px;""")
                    self.button_solutions.setEnabled(False)
                    break
            if symbol == ')':
                check_t = True
                time_t += symbol
            if check_t:
                time_t += symbol
            if check_t and symbol == '(':
                check_t = False
                if ' ' not in time_t or time_t.count(' ') != 1:
                    self.input_posistions.setStyleSheet("""background-color: #E52B50; max-width: 200px;""")
                    time_t = ''
                    self.button_solutions.setEnabled(False)
                    break
            else:
                self.input_posistions.setStyleSheet("""background-color: #26E33B; max-width: 200px;""")
                self.button_solutions.setEnabled(True)
        if text == '':
            self.input_posistions.setStyleSheet("""background-color: none; max-width: 200px;""")
            self.button_solutions.setEnabled(True)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Chess()
    window.show()
    sys.exit(app.exec())