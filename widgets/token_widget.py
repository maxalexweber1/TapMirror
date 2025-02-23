from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel,QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QTimer
from api.taptools_api import get_token_by_id, get_token_price_by_id, get_token_price_chg
from api.xerberus_api import get_risk_score
from widgets.token_chart_widget import TokenChartWidget
from config.config import TOKEN_ID_MAPPING, TOKEN_PRINT_MAPPING
import os

class TokenWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.token_widgets = {}
        self.initUI()

        refresh = self.config.get("refresh", 100000)
        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(refresh)

    def initUI(self):
        layout = QVBoxLayout()
        inner_widgets = self.config["innerWidgets"]
        font_size = self.config.get("font_size", 50)
        color = self.config.get("color", "white")
        pic_scale = self.config.get("images_size",20)
        style = f"font-size: {font_size}px; color: {color};"
        chart_l, chart_h = self.config["chart_size"]

        for ticker in self.config["tokens"]:
            grid = QGridLayout()
            widget_dict = {}
            if "logo" in inner_widgets:
                image_label = QLabel()
                image_path = f"assets/{ticker}.png"
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path).scaled(pic_scale, pic_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    image_label.setPixmap(pixmap)
                else:
                    image_label.setText("[No Image]")
                image_label.setFixedSize(pic_scale, pic_scale)
                image_label.setAlignment(Qt.AlignVCenter)
                grid.addWidget(image_label)
                grid.setColumnMinimumWidth(0, pic_scale)
                widget_dict["image"] = image_label

            if "ticker" in inner_widgets:
                ticker_label = QLabel(f"{ticker}")
                ticker_label.setStyleSheet(style)
                ticker_label.setAlignment(Qt.AlignVCenter)
                grid.addWidget(ticker_label, 0, 1)
                grid.setColumnMinimumWidth(1, 100)
                widget_dict["ticker"] = ticker_label

            if "price" in inner_widgets:
                price_label = QLabel("Loading... ₳")
                price_label.setStyleSheet(style)
                price_label.setAlignment(Qt.AlignVCenter)
                grid.addWidget(price_label, 0, 1)
                grid.setColumnMinimumWidth(1, 200)
                widget_dict["price"] = price_label

            if "riskrating" in inner_widgets:
                risk_image_label = QLabel()    
                fingerprint =  TOKEN_PRINT_MAPPING.get(ticker)
                riskating_data = get_risk_score (fingerprint)
                if riskating_data:
                    token_rating = riskating_data.get('risk_category') 
                    rating_image_path = f"assets/risk_ratings/{token_rating}.png"
                    if os.path.exists(rating_image_path):
                        pixmap = QPixmap(rating_image_path).scaled(pic_scale, pic_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        risk_image_label.setPixmap(pixmap)
                    else:
                       risk_image_label.setText("[N/A]")
                       risk_image_label.setFixedSize(pic_scale, pic_scale)
                       risk_image_label.setAlignment(Qt.AlignVCenter)
                    grid.addWidget(risk_image_label, 0, 2)
                    grid.setColumnMinimumWidth(2, 70)
                    widget_dict["risk_image"] = risk_image_label

            if "change" in inner_widgets:
                change_label = QLabel("Loading...")
                change_label.setStyleSheet(style)
                change_label.setAlignment(Qt.AlignVCenter)
                grid.addWidget(change_label, 0, 3)
                grid.setColumnMinimumWidth(3, 300)
                widget_dict["change"] = change_label

            if "chart" in inner_widgets:
                chart_widget = TokenChartWidget(self)
                chart_widget.setFixedSize(chart_l, chart_h)
                grid.addWidget(chart_widget, 0, 4)
                grid.setColumnMinimumWidth(4, 300)
                widget_dict["chart"] = chart_widget

            layout.addLayout(grid)
            self.token_widgets[ticker] = widget_dict

        self.setLayout(layout)

    def update_data(self, data=None):
        for ticker, elements in self.token_widgets.items():
            price_label = elements.get("price") 
            chart_widget = elements.get("chart")
            change_label = elements.get("change")

            token_id = TOKEN_ID_MAPPING.get(ticker)
            if price_label and token_id:
                token_data = get_token_by_id(token_id)

            if token_data:
                price = round(float(token_data.get("price", 0)), 4)
                price_text = f"{price:>10.4f} ₳"
                price_label.setText(price_text)

            if chart_widget:
                price_data = get_token_price_by_id(token_id, "1D", 7)
                chart_widget.update_chart(price_data)

            if change_label:
                change_data = get_token_price_chg(token_id, "1h", "4h", "24h")
                ch_1 = round(float(change_data.get("1h")) * 100, 2)
                ch_2 = round(float(change_data.get("4h")) * 100, 2)
                ch_3 = round(float(change_data.get("24h")) * 100, 2)
                change_label.setText(f"1h: {ch_1:>5.2f}% 4h: {ch_2:>5.2f}% 24h: {ch_3:>5.2f}%")

                


