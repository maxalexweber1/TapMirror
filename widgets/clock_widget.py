from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from datetime import datetime

class ClockWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        font_size = self.config.get("font_size", 50)
        color = self.config.get("color", "white")
        style = f"font-size: {font_size}px; color: {color};"

        self.label = QLabel("Loading time...")
        self.label.setStyleSheet(style)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def update_data(self, data=None): 
        self.label.setText(datetime.now().strftime("%H:%M:%S"))