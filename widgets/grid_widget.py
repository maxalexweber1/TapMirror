import json
from PyQt5.QtWidgets import QWidget, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt
from widgets.widget_factory import WidgetFactory
from widgets.style_manager import StyleManager

class GridWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config if isinstance(config, dict) else {"grid_sections": config}
        #self.style_manager = StyleManager()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        self.widgets = []

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
                if col == 0 and widget_type != "welcome" and widget_type != "clock":
                    layout.addWidget(widget, row, col, alignment=Qt.AlignLeft)
                else:
                    layout.addWidget(widget, row, col, alignment=Qt.AlignRight)

                self.widgets.append(widget)
        self.setLayout(layout)

    def update_data(self):
        """Initial update for all widgets in the grid."""
        for widget in self.widgets:
            if hasattr(widget, 'update_data'):
                widget.update_data()