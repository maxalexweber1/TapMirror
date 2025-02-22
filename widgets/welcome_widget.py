from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime

class WelcomeWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()
        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(1000)

    def initUI(self):
        layout = QVBoxLayout()
        font_size = self.config.get("font_size", 50)
        color = self.config.get("color", "white")
        style = f"font-size: {font_size}px; color: {color};"

        self.label = QLabel("Loading...")
        self.label.setStyleSheet(style)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def get_greeting(self):
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning!"
        elif hour < 18:
            return "Good afternoon!"
        else:
            return "Good evening!"

    def update_data(self, data=None):
        greeting = self.get_greeting()
        self.label.setText(greeting)