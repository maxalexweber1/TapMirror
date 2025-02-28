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
        self.setStyleSheet("background-color: black; color: white; border: none;")  # Dark theme, no borders
        self.update_data()

    def initUI(self):
        """Ensures the header stays in a single row and auto-sizes to content."""
        layout = QHBoxLayout()
        layout.setSpacing(15)  # Spacing between widgets
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # Ensure vertical centering

        for section in self.config:
            widget = None

            if section["type"] == "clock":
                widget = ClockWidget(section)
            elif section["type"] == "marketdata":
                widget = MarketDataWidget(section)

            if widget:
                container = QFrame()  # Wrap widget to ensure same height
                container.setStyleSheet("background-color: transparent; border: none;")  # No extra borders
                container_layout = QHBoxLayout()
                container_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
                container_layout.setAlignment(Qt.AlignVCenter)  # Vertical alignment fix
                container_layout.addWidget(widget)
                container.setLayout(container_layout)
                
                self.header_elements[section["type"]] = widget
                layout.addWidget(container)

        layout.addStretch()  # Ensures elements don’t expand unevenly
        self.setLayout(layout)
        self.adjustSize()  # Ensure widget sizes dynamically

    def update_data(self):
        """Updates data for all header elements."""
        for key, widget in self.header_elements.items():
            try:
                widget.update_data()
            except Exception as e: 
                print(f"Error updating {key}: {e}")
