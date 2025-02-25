import json
from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from widgets.clock_widget import ClockWidget
from widgets.market_data_widget import MarketDataWidget

class HeaderWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.header_elements = {}
        self.initUI()
        self.update_data()
    def initUI(self):
        layout = QHBoxLayout()

        for section in self.config:

            section_frame = QFrame()
            section_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
            section_frame.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; background-color: #000000;"
            )
            if section["type"] == "clock":
                widget = ClockWidget(section)
                self.header_elements["clock"] = widget
            elif section["type"] == "marketdata":
                widget = MarketDataWidget(section)
                self.header_elements["market_data"] = widget


            frame_layout = QVBoxLayout()
            frame_layout.addWidget(widget)
            section_frame.setLayout(frame_layout)
            layout.addWidget(section_frame)

        self.setLayout(layout)

    def update_data(self):
        for key, widget in self.header_elements.items():
            try:
                widget.update_data()
            except Exception as e: 
                print(f"Error while Update: {key}: {e}")