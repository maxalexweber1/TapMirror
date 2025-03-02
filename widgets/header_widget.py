from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
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
        layout.setSpacing(30) 
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        for section in self.config:
            widget = None

            if section["type"] == "clock":
                widget = ClockWidget(section)
            elif section["type"] == "market_data":
                widget = MarketDataWidget(section)

            if widget:
                container = QFrame() 
                container_layout = QHBoxLayout()
                container_layout.setContentsMargins(0, 0, 0, 0)  
                container_layout.setAlignment(Qt.AlignVCenter)
                container_layout.addWidget(widget)
                container.setLayout(container_layout)
                
                self.header_elements[section["type"]] = widget
                layout.addWidget(container)

        layout.addStretch() 
        self.setLayout(layout)
        self.adjustSize()  

    def update_data(self):
        """Updates data for all header elements."""
        for key, widget in self.header_elements.items():
            try:
                widget.update_data()
            except Exception as e: 
                print(f"Error updating {key}: {e}")
