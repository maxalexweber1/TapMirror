import json
import os
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from api import get_token_by_id, get_market_stats, get_token_price_by_id,get_quote_price
from config import TOKEN_MAPPING, UPDATE_INTERVAL, GRID_SIZE
from chart_widget import ChartWidget

# Load UI layout from JSON config file
def load_layout_config():
    """Loads the layout configuration from a JSON file."""
    with open("layout_config.json", "r") as file:
        return json.load(file)

class TapMirrorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.config = load_layout_config()
        self.ui_elements = {}  # Store references to UI elements

        self.initUI()
        self.update_data()

        # Timer for automatic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(UPDATE_INTERVAL)

    def initUI(self):
        """Sets up the UI dynamically based on the JSON configuration."""
        self.setWindowTitle("TapMirror")
        self.setGeometry(0, 0, 800, 480)
        self.showFullScreen()

        layout = QGridLayout()
        layout.setSpacing(5)

        for section in self.config["sections"]:
            row, col = section["position"]
            section_frame = QFrame()
            section_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
            section_frame.setStyleSheet("border: 1px solid red;")
            section_layout = QVBoxLayout(section_frame)

            if section["type"] == "tokens":
                show_options = section.get("show", [])
                token_vbox = QVBoxLayout()
                token_widgets = {}

                for ticker in section["tokens"]:
                    token_hbox = QHBoxLayout()

                    # Token-Logo (falls in "show" enthalten)
                    image_label = QLabel()
                    if "logo" in show_options:
                        image_path = f"assets/{ticker}.png"
                        if os.path.exists(image_path):
                            pixmap = QPixmap(image_path).scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            image_label.setPixmap(pixmap)
                        else:
                            image_label.setText("[No Image]")
                        image_label.setFixedSize(70, 70)
                        image_label.setAlignment(Qt.AlignVCenter)
                        token_hbox.addWidget(image_label)

                    # Token-Preis (falls in "show" enthalten)
                    price_label = QLabel(f"{ticker}: Loading...")
                    price_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                    price_label.setAlignment(Qt.AlignVCenter)
                    if "price" in show_options:
                        token_hbox.addWidget(price_label)
                        token_vbox.addLayout(token_hbox)  # Fügt Token-Preis und Logo hinzu

                    # Chart-Widget (falls in "show" enthalten)
                    chart_widget = None
                    if "chart" in show_options:
                        chart_widget = ChartWidget(self)
                        chart_widget.setFixedSize(300, 150)
                    if chart_widget:
                        token_hbox.addWidget(chart_widget)  # Fügt Chart unten hinzu
                    # Speichert die UI-Elemente für spätere Updates
                    token_widgets[ticker] = {"image": image_label, "price": price_label, "chart": chart_widget}

                # Speichert die gesamte Token-Sektion
                self.ui_elements[f"tokens_{row}_{col}"] = token_widgets
                section_layout.addLayout(token_vbox)

            elif section["type"] == "clock":
                label = QLabel("Loading time...")
                label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                label.setAlignment(Qt.AlignCenter)
                self.ui_elements[f"clock_{row}_{col}"] = {"label": label}
                section_layout.addWidget(label)

            elif section["type"] == "market_data":
                label = QLabel("Loading market data...")
                label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                label.setAlignment(Qt.AlignCenter)
                self.ui_elements[f"market_{row}_{col}"] = {"label": label, "fields": section["fields"]}
                section_layout.addWidget(label)

            elif section["type"] == "quote":
                quote_label = QLabel()
                quote_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                quote_label.setAlignment(Qt.AlignCenter)
                # Speichere das Label, damit update_data() es später aktualisieren kann
                self.ui_elements[f"quote_{row}_{col}"] = {"label": quote_label}
                section_layout.addWidget(quote_label)

            section_frame.setLayout(section_layout)
            layout.addWidget(section_frame, row, col)

        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")

    def update_data(self):
        """Fetches API data and updates the UI elements dynamically."""
        
        # Update token prices + Charts
        for key, token_widgets in self.ui_elements.items():
            if key.startswith("tokens"):
                for ticker, elements in token_widgets.items():
                    price_label = elements.get("price")
                    chart_widget = elements.get("chart")

                    token_id = TOKEN_MAPPING.get(ticker)
                    if price_label and token_id:
                        token_data = get_token_by_id(token_id)
                        if token_data:
                            price = round(float(token_data.get("price", 0)), 4)
                            price_label.setText(f"{ticker}: {price} ₳")

                    # Falls Charts vorhanden sind, aktualisiere sie
                    if chart_widget:
                        price_data = get_token_price_by_id(token_id, "1D", 7)
                        chart_widget.update_chart(price_data)
        # Update clock
        for key, elements in self.ui_elements.items():
            if key.startswith("clock"):
                label = elements.get("label")
                if label:
                    label.setText(datetime.now().strftime("%H:%M:%S"))

        # Update market data
        market_data = get_market_stats("ADA")
        for key, elements in self.ui_elements.items():
            if key.startswith("market") and market_data:
                label = elements.get("label")
                fields = elements.get("fields", [])
                if label and fields:
                    text = "\n".join([f"{field}: {market_data.get(field, 'N/A')}" for field in fields])
                    label.setText(text)

        # Update quote data
        quote_data = get_quote_price("USD")
        for key, elements in self.ui_elements.items():
            if key.startswith("quote") and quote_data:
                quote_label = elements.get("label")
                if "price" in quote_data:
                    price = round(float(quote_data.get("price", 0)), 4)
                    quote_label.setText(f"ADA Price: {price} $")
                else:
                    quote_label.setText("ADA Price: N/A")         

    def keyPressEvent(self, event):
        """Allows the ESC key to exit the application."""
        if event.key() == Qt.Key_Escape:
            self.close()  # Closes the application
