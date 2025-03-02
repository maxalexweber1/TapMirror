import json
from typing import Any, Tuple, List, Optional
from PyQt5.QtWidgets import QApplication

class StyleManager:
    """Singleton class to manage UI styles and scaling based on JSON configuration."""

    _instance = None 

    def __new__(cls) -> "StyleManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """Loads the layout configuration from a JSON file. Uses default if file is missing or invalid."""
        default_config = {
            "grid_sections": [],
            "header_sections": [],
            "grid_structure": [4, 4],
            "scaling_base": {
                "reference_width": 1920, 
                "min_factor": 0.8,      
                "max_factor": 2.0 
            }
        }
        try:
            with open("./config/layout_config.json", "r") as file:
                self.config = json.load(file)
                
            if not isinstance(self.config.get("grid_sections"), list) or \
               not isinstance(self.config.get("header_sections"), list):
                self.config = default_config
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            self.config = default_config

    def get_style(self, section_type: str, key: str, default: Any = None) -> Any:
        """ Retrieves the style value for a specific section type"""

        for section in self.config.get("grid_sections", []) + self.config.get("header_sections", []):
            if section.get("type") == section_type:
                return section.get(key, default)
        return default

    def get_screen_size(self) -> Tuple[int, int]:
        """Returns the screen size as a tuple (width, height)."""
        screen = QApplication.primaryScreen()
        size = screen.size()
        return size.width(), size.height()

    def get_scaling_factor(self) -> float:
        """ Calculates a dynamic scaling factor based on screen width compared to a reference width """
        width, _ = self.get_screen_size()

        scaling_base = self.config.get("scaling_base", {
            "reference_width": 1536,
            "min_factor": 0.5,
            "max_factor": 2.0
        })

        reference_width = scaling_base.get("reference_width", 1536)
        min_factor = scaling_base.get("min_factor", 0.5)
        max_factor = scaling_base.get("max_factor", 2.0)

        factor = width / reference_width

        return max(min_factor, min(max_factor, factor))

    def get_scaled_value(self, section_type: str, key: str, default_value: float) -> int:
        """Scales a numeric value based on screen size"""

        base_value = self.get_style(section_type, key, default_value)

        if isinstance(base_value, (int, float)):
            scaling_factor = self.get_scaling_factor()
            print(scaling_factor)
            return int(base_value * scaling_factor)
        return base_value  

    def get_scaled_font_size(self, section_type: str) -> int:
        """Returns the scaled font size for a section."""
        return self.get_scaled_value(section_type, "font_size", 30)

    def get_scaled_header_size(self, section_type: str) -> int:
        """Returns the scaled font size for a header section."""
        return self.get_scaled_value(section_type, "font_size", 35)

    def get_scaled_image_size(self, section_type: str, key: str = "image_size") -> int:
        """Returns the scaled image size for a section (e.g., image_size, fc_image_size)."""
        return self.get_scaled_value(section_type, key, 50)

    def get_scaled_chart_size(self, section_type: str) -> List[int]:
        """Returns the scaled chart size for a widget type."""
        base_size = self.get_style(section_type, "chart_size", [180, 140])
        scaling_factor = self.get_scaling_factor()
        return [int(dim * scaling_factor) for dim in base_size]

    def get_fixed_grid_structure(self) -> List[int]:
        """Returns the fixed grid structure from the configuration."""
        return self.config.get("grid_structure", [4, 4])

    def get_layout_config(self) -> dict:
        """Returns the entire layout configuration."""
        return self.config
    
    def format_number(n):
        """Returns the entire layout configuration."""
        if n >= 1_000_000:
            million_value = n / 1_000_000
            if million_value.is_integer():
                million_str = f"{int(million_value)}"
            else:
                million_str = f"{million_value:.1f}".replace(',', '.')
            return f"{million_str} Mio"
        else:
            return f"{n:,}".replace(",", ".")