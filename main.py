import sys
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # ===== 1. НАСТРОЙКА ОКНА =====
        self.setWindowTitle('Расширенное приложение')
        self.setGeometry(100, 100, 600, 400)
        
        # ===== 2. МЕНЮ (QMenuBar) =====
        menu_bar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menu_bar.addMenu('Файл')
        exit_action = file_menu.addAction('Выход')
        exit_action.triggered.connect(self.close)
        
        # Меню "Справка"
        help_menu = menu_bar.addMenu('Справка')
        about_action = help_menu.addAction('О программе')
        about_action.triggered.connect(self.show_about_dialog)
        
        # ===== 3. ВКЛАДКИ (QTabWidget) =====
        tabs = QTabWidget()
        
        # ---- Вкладка 1: Ввод данных ----
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        
        self.label = QLabel('Введите ваше имя:')
        self.text_field = QLineEdit()
        self.button = QPushButton('Отправить')
        self.button.clicked.connect(self.on_button_click)
        self.result_label = QLabel('Результат:')
        
        tab1_layout.addWidget(self.label)
        tab1_layout.addWidget(self.text_field)
        tab1_layout.addWidget(self.button)
        tab1_layout.addWidget(self.result_label)
        tab1.setLayout(tab1_layout)
        
        # ---- Вкладка 2: Информация ----
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(QLabel('Информация о приложении'))
        tab2_layout.addWidget(QLabel('Это пример с меню, вкладками и диалогами'))
        tab2.setLayout(tab2_layout)
        
        # Добавляем вкладки
        tabs.addTab(tab1, 'Главная')
        tabs.addTab(tab2, 'О программе')
        
        self.setCentralWidget(tabs)
        
        # ===== 4. ДИАЛОГОВОЕ ОКНО ПРИ ЗАПУСКЕ =====
        self.show_welcome_dialog()
    
    # ===== ОБРАБОТЧИК КНОПКИ =====
    def on_button_click(self):
        name = self.text_field.text()
        if name:
            self.result_label.setText(f'Результат: Привет, {name}!')
            self.text_field.clear()
        else:
            self.result_label.setText('⚠️ Введите имя!')
    
    # ===== ДИАЛОГ ПРИВЕТСТВИЯ =====
    def show_welcome_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Добро пожаловать')
        msg.setText('Добро пожаловать в приложение!')
        msg.setInformativeText('Используйте меню, вкладки и поле ввода.')
        msg.exec_()
    
    # ===== ДИАЛОГ "О ПРОГРАММЕ" =====
    def show_about_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('О программе')
        msg.setText('Приложение создано для лабораторной работы №3')
        msg.setInformativeText('PyQt5\nВерсия 1.0')
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
