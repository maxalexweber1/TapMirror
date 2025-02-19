from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from api.api import get_token_by_id, get_token_price_by_id, get_token_price_chg
from widgets.chart_widget import ChartWidget
from config.config import TOKEN_MAPPING
import os

class TokenWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.token_widgets = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        show_options = self.config.get("show", self.config.get("innerWidgets", []))
        font_size = self.config.get("font_size", 50)
        color = self.config.get("color", "white")
        style = f"font-size: {font_size}px; color: {color};"

        for ticker in self.config["tokens"]:
            token_hbox = QHBoxLayout()
            widget_dict = {}

            if "logo" in show_options:
                image_label = QLabel()
                image_path = f"assets/{ticker}.png"
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path).scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    image_label.setPixmap(pixmap)
                else:
                    image_label.setText("[No Image]")
                image_label.setFixedSize(70, 70)
                image_label.setAlignment(Qt.AlignVCenter)
                token_hbox.addWidget(image_label)
                widget_dict["image"] = image_label

            if "price" in show_options:
                price_label = QLabel(f"{ticker}: Loading...")
                price_label.setStyleSheet(style)
                price_label.setAlignment(Qt.AlignVCenter)
                token_hbox.addWidget(price_label)
                widget_dict["price"] = price_label

            if "change" in show_options:
                change_label = QLabel("Loading...")
                change_label.setStyleSheet(style)
                change_label.setAlignment(Qt.AlignVCenter)
                token_hbox.addWidget(change_label)
                widget_dict["change"] = change_label

            if "chart" in show_options:
                chart_widget = ChartWidget(self)
                chart_widget.setFixedSize(300, 150)
                token_hbox.addWidget(chart_widget)
                widget_dict["chart"] = chart_widget

            layout.addLayout(token_hbox)
            self.token_widgets[ticker] = widget_dict

        self.setLayout(layout)

    def update_data(self, data=None):  # Optionaler Parameter
        for ticker, elements in self.token_widgets.items():
            price_label = elements.get("price")
            chart_widget = elements.get("chart")
            change_label = elements.get("change")

            token_id = TOKEN_MAPPING.get(ticker)
            if price_label and token_id:
                token_data = get_token_by_id(token_id)
                if token_data:
                    price = round(float(token_data.get("price", 0)), 4)
                    price_label.setText(f"{ticker}: {price} ₳")
            if chart_widget:
                price_data = get_token_price_by_id(token_id, "1D", 7)
                chart_widget.update_chart(price_data)
            if change_label:
                change_data = get_token_price_chg(token_id, "1h", "4h", "24h")
                ch_1 = round(float(change_data.get("1h")) * 100, 2)
                ch_2 = round(float(change_data.get("4h")) * 100, 2)
                ch_3 = round(float(change_data.get("24h")) * 100, 2)
                change_label.setText(f"1h: {ch_1}% 4h: {ch_2}% 24h: {ch_3}%")