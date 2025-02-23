from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime


class ClockWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()

        refresh = self.config.get("refresh", 1000)
        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(refresh)

    def initUI(self):
        layout = QVBoxLayout()
        font_size = self.config.get("font_size", 20)
        color = self.config.get("color", "white")
        style = f"font-size: {font_size}px; color: {color};"

        self.label = QLabel("Loading time...")
        self.label.setStyleSheet(style)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def update_data(self, data=None): 
        self.label.setText(datetime.now().strftime("%H:%M:%S"))