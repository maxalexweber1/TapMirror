from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from config.config import TOKEN_ID_MAPPING
from datetime import datetime
from api.taptools_api import get_last_token_trades
from widgets.style_manager import StyleManager
import os

class TokenTradesWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.style_manager = StyleManager()
        self.initUI()

        refresh = self.config.get("refresh", 100000)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(refresh)
        self.update_data()

    def initUI(self):
        layout = QVBoxLayout()
        font_size = self.style_manager.get_scaled_font_size("token_trades")
        color = self.style_manager.get_style("token_trades", "color", "white")
        header_size = self.style_manager.get_scaled_font_size("token_trades")
        
        frame = QFrame()
        frame.setStyleSheet("border: 2px solid white; border-radius: 5px;")
        frame_layout = QVBoxLayout()
        
        self.trade_table = QGridLayout()
        headers = ["Token", "Action", "Amount", "ADA", "Price", "Time"]
        
        # Ensure headers are re-added
        for col_idx, header in enumerate(headers):
            trade_header_label = QLabel(header)
            trade_header_label.setStyleSheet(f"font-size: {header_size}px; color: {color}; font-weight: bold;")
            trade_header_label.setAlignment(Qt.AlignCenter)
            self.trade_table.addWidget(trade_header_label, 0, col_idx)
        
        frame_layout.addLayout(self.trade_table)
        frame.setLayout(frame_layout)
        layout.addWidget(frame)
        self.setLayout(layout)

    def update_data(self):
        self._clear_trade_rows()
        
        font_size = self.style_manager.get_scaled_font_size("token_trades")
        color = self.style_manager.get_style("token_trades", "color", "white")
        trade_count = self.config.get("count", 10)
        ticker = self.config.get("ticker", "ADA")
        value = self.config.get("value", 1)
        
        token_id = TOKEN_ID_MAPPING.get(ticker, "Unknown")
        last_trades_data = get_last_token_trades("24h", token_id, value, "time", trade_count)
        last_trades = LastTrades(last_trades_data).trades
        
        if not last_trades:
            return
        
        # Re-add headers before adding rows
        headers = ["Token", "Action", "Amount", "ADA", "Price", "Time"]
        for col_idx, header in enumerate(headers):
            trade_header_label = QLabel(header)
            trade_header_label.setStyleSheet(f"font-size: {font_size}px; color: {color}; font-weight: bold;")
            trade_header_label.setAlignment(Qt.AlignCenter)
            self.trade_table.addWidget(trade_header_label, 0, col_idx)
        
        for row_idx, trade in enumerate(last_trades, start=1):
            self._add_trade_row(trade, row_idx, font_size, color)

    def _clear_trade_rows(self):
        for i in range(self.trade_table.count() - 1, -1, -1):
            item = self.trade_table.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
                self.trade_table.removeWidget(item.widget())

    def _add_trade_row(self, trade, row_idx, font_size, color):
        pic_scale = self.style_manager.get_scaled_value("token_trades", "images_size", 35)
        image_label = QLabel()
        image_path = os.path.join("assets/token", f"{trade.tokenAName}.png")
        
        pixmap = QPixmap(pic_scale, pic_scale)
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(pic_scale, pic_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        self.trade_table.addWidget(image_label, row_idx, 0)
        
        now = datetime.now()
        trade_time = datetime.fromtimestamp(trade.time)
        delta_time = (now - trade_time).total_seconds()
        
        if delta_time <= 60:
            time_ago = f"{delta_time:.0f}s ago"
        elif delta_time <= 3600:
            time_ago = f"{round(delta_time / 60)}m ago"
        elif delta_time <= 86400:
            time_ago = f"{round(delta_time / 3600)}h ago"
        else:
            time_ago = f"{round(delta_time / 86400)} days ago"
        
        action_color = "green" if trade.action.lower() == "buy" else "red" if trade.action.lower() == "sell" else color
        
        labels = [
            (trade.action, 1, action_color),
            (f"{round(float(trade.tokenAAmount))}", 2),
            (f"{round(float(trade.tokenBAmount))}", 3),
            (f"{round(float(trade.price), 3)}", 4),
            (time_ago, 5),
        ]
        
        for label_data in labels:
            text = label_data[0]
            col_idx = label_data[1]
            label_color = label_data[2] if len(label_data) > 2 else color
            
            label = QLabel(str(text))
            label.setStyleSheet(f"font-size: {font_size}px; color: {label_color};")
            label.setAlignment(Qt.AlignCenter)
            self.trade_table.addWidget(label, row_idx, col_idx)

class LastTrades:
    def __init__(self, data):
        self.trades = [Trade(tr) for tr in data]

class Trade:
    def __init__(self, data):
        self.action = data.get("action")
        self.time = data.get("time")
        self.price = data.get("price")
        self.tokenAName = data.get("tokenAName")
        self.tokenAAmount = data.get("tokenAAmount")
        self.tokenBName = data.get("tokenBName")
        self.tokenBAmount = data.get("tokenBAmount")