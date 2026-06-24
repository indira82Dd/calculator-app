import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from datetime import datetime

# ============================================================
#  МОДУЛЬ 1: РАБОТА С БАЗОЙ ДАННЫХ (Database)
# ============================================================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('app_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                date TEXT
            )
        ''')
        self.conn.commit()
    
    def insert_user(self, name):
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cursor.execute('INSERT INTO users (name, date) VALUES (?, ?)', (name, date))
        self.conn.commit()
    
    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()
    
    def search_users(self, keyword):
        self.cursor.execute('SELECT * FROM users WHERE name LIKE ?', (f'%{keyword}%',))
        return self.cursor.fetchall()
    
    def delete_user(self, user_id):
        self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()
    
    def get_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM users')
        return self.cursor.fetchone()[0]
    
    def close(self):
        self.conn.close()

# ============================================================
#  МОДУЛЬ 2: ГЛАВНОЕ ОКНО (MainWindow)
# ============================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        
        self.setWindowTitle('📚 Моя записная книжка')
        self.setGeometry(100, 100, 650, 500)
        self.setMinimumSize(500, 400)
        
        # ===== МЕНЮ =====
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('📁 Файл')
        exit_action = file_menu.addAction('🚪 Выход')
        exit_action.triggered.connect(self.close)
        
        help_menu = menu_bar.addMenu('❓ Справка')
        about_action = help_menu.addAction('📖 О программе')
        about_action.triggered.connect(self.show_about)
        
        # ===== ВКЛАДКИ =====
        tabs = QTabWidget()
        
        # --- ВКЛАДКА 1: ДОБАВЛЕНИЕ ---
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        
        self.label = QLabel('✏️ Введите имя:')
        self.text_field = QLineEdit()
        self.text_field.setPlaceholderText('Например: Анна')
        self.save_button = QPushButton('💾 Сохранить в БД')
        self.save_button.setStyleSheet('background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;')
        self.save_button.clicked.connect(self.save_data)
        self.result_label = QLabel('📌 Результат:')
        self.result_label.setStyleSheet('font-size: 14px;')
        
        tab1_layout.addWidget(self.label)
        tab1_layout.addWidget(self.text_field)
        tab1_layout.addWidget(self.save_button)
        tab1_layout.addWidget(self.result_label)
        tab1_layout.addStretch()
        tab1.setLayout(tab1_layout)
        
        # --- ВКЛАДКА 2: ПРОСМОТР ---
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        
        # Панель инструментов
        toolbar = QHBoxLayout()
        self.view_button = QPushButton('📋 Показать всё')
        self.view_button.clicked.connect(self.show_data)
        self.sort_button = QPushButton('🔤 Сортировка А→Я')
        self.sort_button.clicked.connect(self.show_sorted_data)
        self.count_label = QLabel('📊 Всего: 0')
        
        toolbar.addWidget(self.view_button)
        toolbar.addWidget(self.sort_button)
        toolbar.addWidget(self.count_label)
        toolbar.addStretch()
        
        # Поиск
        search_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText('🔍 Поиск по имени...')
        self.search_field.textChanged.connect(self.search_data)
        search_layout.addWidget(self.search_field)
        
        # Область вывода
        self.data_label = QLabel('📭 Нажмите "Показать всё"')
        self.data_label.setWordWrap(True)
        self.data_label.setStyleSheet('font-size: 13px; padding: 10px; background-color: #f9f9f9; border-radius: 5px;')
        
        # Удаление
        delete_layout = QHBoxLayout()
        self.delete_field = QLineEdit()
        self.delete_field.setPlaceholderText('Введите ID для удаления')
        self.delete_button = QPushButton('🗑️ Удалить')
        self.delete_button.setStyleSheet('background-color: #f44336; color: white; font-weight: bold;')
        self.delete_button.clicked.connect(self.delete_data)
        
        delete_layout.addWidget(QLabel('ID:'))
        delete_layout.addWidget(self.delete_field)
        delete_layout.addWidget(self.delete_button)
        
        tab2_layout.addLayout(toolbar)
        tab2_layout.addLayout(search_layout)
        tab2_layout.addWidget(self.data_label)
        tab2_layout.addLayout(delete_layout)
        tab2.setLayout(tab2_layout)
        
        tabs.addTab(tab1, '➕ Добавить')
        tabs.addTab(tab2, '📂 Просмотр')
        
        self.setCentralWidget(tabs)
        
        self.show_welcome()
        self.update_count()
    
    # ===== МЕТОДЫ =====
    def save_data(self):
        name = self.text_field.text().strip()
        if name:
            self.db.insert_user(name)
            self.result_label.setText(f'✅ Имя "{name}" сохранено!')
            self.text_field.clear()
            self.update_count()
        else:
            self.result_label.setText('⚠️ Введите имя!')
    
    def show_data(self):
        users = self.db.get_all_users()
        self.display_users(users)
    
    def show_sorted_data(self):
        users = self.db.get_all_users()
        if users:
            sorted_users = sorted(users, key=lambda x: x[1])
            self.display_users(sorted_users, '🔤 Отсортировано по алфавиту:\n\n')
        else:
            self.data_label.setText('📭 Нет записей')
    
    def search_data(self):
        keyword = self.search_field.text().strip()
        if keyword:
            users = self.db.search_users(keyword)
            if users:
                self.display_users(users, f'🔍 Результаты поиска "{keyword}":\n\n')
            else:
                self.data_label.setText(f'🔍 Ничего не найдено для "{keyword}"')
        else:
            self.show_data()
    
    def delete_data(self):
        try:
            user_id = int(self.delete_field.text())
            self.db.delete_user(user_id)
            self.delete_field.clear()
            self.show_data()
            self.update_count()
        except:
            self.data_label.setText('⚠️ Введите корректный ID!')
    
    def display_users(self, users, title='📋 Все записи:\n\n'):
        if users:
            text = title
            for user in users:
                text += f'🔹 ID: {user[0]} | Имя: {user[1]} | 🕐 {user[2]}\n'
            self.data_label.setText(text)
        else:
            self.data_label.setText('📭 Нет записей')
    
    def update_count(self):
        count = self.db.get_count()
        self.count_label.setText(f'📊 Всего: {count}')
    
    def show_welcome(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('👋 Добро пожаловать!')
        msg.setText('📚 Моя записная книжка')
        msg.setInformativeText(
            '💡 Возможности:\n'
            '• Добавляйте имена\n'
            '• Ищите по имени\n'
            '• Сортируйте по алфавиту\n'
            '• Удаляйте записи\n'
            '• Все данные сохраняются в БД'
        )
        msg.exec_()
    
    def show_about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('📖 О программе')
        msg.setText('📚 Моя записная книжка')
        msg.setInformativeText(
            'Версия: 2.0\n'
            'Сделано для лабораторной работы №4\n'
            '💾 База данных: SQLite\n'
            '🎨 Интерфейс: PyQt5\n'
            '📦 Сборка: PyInstaller'
        )
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
