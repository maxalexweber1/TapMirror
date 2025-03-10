from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QFrame, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime
from widgets.style_manager import StyleManager

class ClockWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.style_manager = StyleManager()
        self.initUI()

        refresh = self.config.get("refresh", 1000)
        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(refresh)

    def initUI(self):
        layout = QVBoxLayout()
        font_size = self.style_manager.get_scaled_font_size("clock") 
        color = self.style_manager.get_style("clock", "color", "white")
        frame_style = "border: none;"
        style = f"font-size: {font_size}px; color: {color}; border: none;"

        clock_frame = QFrame()
        clock_frame.setStyleSheet(frame_style)
        clock_layout = QHBoxLayout()
        clock_layout.setContentsMargins(0, 0, 0, 0)
        clock_layout.setSpacing(0)
        self.label = QLabel("Loading time...")
        self.label.setStyleSheet(style)
        self.label.setAlignment(Qt.AlignCenter)
        clock_layout.addWidget(self.label)
        clock_frame.setLayout(clock_layout)

        layout.addWidget(clock_frame)
        self.setLayout(layout)

    def update_data(self, data=None):
        """Update Time""" 
        self.label.setText(datetime.now().strftime("%H:%M:%S"))
