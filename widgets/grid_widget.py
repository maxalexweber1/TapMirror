import json
from PyQt5.QtWidgets import QWidget, QGridLayout, QSizePolicy, QApplication
from PyQt5.QtCore import Qt
from widgets.widget_factory import WidgetFactory
from widgets.style_manager import StyleManager

class GridWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config if isinstance(config, dict) else {"grid_sections": config}
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.widgets = []

        screen = QApplication.primaryScreen()
        screen_height = screen.availableGeometry().height()
        half_screen_height = screen_height // 2
    
        max_row = 0
        max_col = 0
        for section in self.config.get("grid_sections", []):
            if not isinstance(section, dict):
                print(f"Warning: Invalid section format: {section}")
                continue
            row, col = section.get("position", [0, 0])
            widget_type = section.get("type")
            if not widget_type:
                print(f"Warning: Missing 'type' key in section: {section}")
                continue
            widget = WidgetFactory.create_widget(widget_type, section)
            if widget:
                widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                if col == 0 and widget_type != "welcome" and widget_type != "clock":
                    layout.addWidget(widget, row, col, alignment=Qt.AlignLeft | Qt.AlignTop)
                else:
                    layout.addWidget(widget, row, col, alignment=Qt.AlignRight | Qt.AlignTop)

                self.widgets.append(widget)
                max_row = max(max_row, row)
                max_col = max(max_col, col)

       
        layout.setRowMinimumHeight(0, half_screen_height)
        for i in range(1, max_row + 1):
            layout.setRowMinimumHeight(i, 50) 
        layout.setRowStretch(max_row + 1, 1)

        for i in range(max_col + 1):
            layout.setColumnMinimumWidth(i, 200)  
            layout.setColumnStretch(i, 1)  
        layout.setColumnStretch(max_col + 1, 0) 

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    def update_data(self):
        """Updates data for all grid elements."""
        for widget in self.widgets:
            if hasattr(widget, 'update_data'):
                widget.update_data()