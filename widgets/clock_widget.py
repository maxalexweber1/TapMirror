from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime
from widgets.style_manager import StyleManager  # Importiere den StyleManager

class ClockWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.style_manager = StyleManager()  # Initialisiere den StyleManager
        self.initUI()

        refresh = self.config.get("refresh", 1000)
        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(refresh)

    def initUI(self):
        layout = QVBoxLayout()
        font_size = self.style_manager.get_scaled_font_size("clock")  # Nutzt den StyleManager für die Schriftgröße
        color = self.style_manager.get_style("clock", "color", "white")  # Farbe aus der config
        style = f"font-size: {font_size}px; color: {color};"

        self.label = QLabel("Loading time...")
        self.label.setStyleSheet(style)
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)

        self.setLayout(layout)

    def update_data(self, data=None): 
        self.label.setText(datetime.now().strftime("%H:%M:%S"))
