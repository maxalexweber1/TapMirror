from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime
from widgets.style_manager import StyleManager

class WelcomeWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.style_manager = StyleManager()
        self.initUI()

        refresh = self.config.get("refresh", 100000)
        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(refresh)

    def initUI(self):
        layout = QVBoxLayout()
        font_size = self.style_manager.get_scaled_font_size("welcome")
        color = self.style_manager.get_style("welcome", "color", "white")
        style = f"font-size: {font_size}px; color: {color}; border: none;"

        self.label = QLabel("Loading...")
        self.label.setStyleSheet(style)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.update_data()

    def get_greeting(self):
        greetings = self.config.get("greetings", {
            "morning": "Good morning!",
            "afternoon": "Good afternoon!",
            "evening": "Good evening!"
        })
        
        hour = datetime.now().hour
        if hour < 12:
            return greetings.get("morning", "Good morning!")
        elif hour < 18:
            return greetings.get("afternoon", "Good afternoon!")
        else:
            return greetings.get("evening", "Good evening!")

    def update_data(self, data=None):
        greeting = self.get_greeting()
        self.label.setText(greeting)
