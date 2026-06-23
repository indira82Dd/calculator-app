import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Моё приложение')
        self.setGeometry(100, 100, 400, 300)
        
        self.label = QLabel('Привет, мир!')
        self.button = QPushButton('Нажми меня')
        self.button.clicked.connect(self.on_button_click)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def on_button_click(self):
        self.label.setText('Кнопка нажата!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
