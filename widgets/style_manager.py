import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

class StyleManager:

    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        """Loads the layout configuration from the JSON file."""
        try:
            with open("./config/layout_config.json", "r") as file:
                self.config = json.load(file)
        except Exception as e:
            print(f"Error loading configuration file: {e}")
            self.config = {}

    def get_style(self, section_type, key, default=None):
        """Retrieves the style value for a specific widget type."""
        for section in self.config.get("grid_sections", []) + self.config.get("header_sections", []):
            if section.get("type") == section_type:
                return section.get(key, default)
        return default

    def get_screen_size(self):
        """Retrieves the screen size."""
        screen = QApplication.primaryScreen()
        size = screen.size()
        return size.width(), size.height()

    def get_scaled_value(self, section_type, key, base_default):
        """Scales values based on the screen size."""
        base_value = self.get_style(section_type, key, base_default)
        width, _ = self.get_screen_size()

        if width > 1920:  # Example for 4K scaling
            return int(base_value * 1.5)
        return int(base_value)

    def get_scaled_font_size(self, section_type):
        """Adjusts the font size based on screen size."""
        return self.get_scaled_value(section_type, "font_size", 30)
    
    def get_scaled_header_size(self, section_type):
        """Adjusts the font size based on screen size."""
        return self.get_scaled_value(section_type, "font_size", 30)

    def get_fixed_grid_structure(self):
        """Retrieves fixed grid structure from config."""
        return self.config.get("grid_structure", [4, 4])  # Default 4x4

    def fade_in(self, widget):
        """Smooth fade-in animation for widgets."""
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(500)  # 500ms animation
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()

    def get_scaled_height(self, section_type):
        """Adjusts the widget height based on screen size."""
        return self.get_scaled_value(section_type, "height", 200)

    def get_layout_config(self):
        """Returns the entire layout configuration."""
        return self.config
    
    def get_scaled_chart_size(self, widget_type):
        return self.get_style(widget_type, "chart_size", [180, 140])