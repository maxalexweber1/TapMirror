from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from config.config import TOKEN_ID_MAPPING
from datetime import datetime
from api.taptools_api import get_last_token_trades


class TokenTradesWidget(QWidget):
    BOLD_STYLE = "font-weight: bold;"

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.token_widgets = {}
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100000)

    def initUI(self):
        layout = QVBoxLayout()
        color = self.config.get("color", "white")
        header_size = self.config["header_size"]

        self.trade_table = QGridLayout()
        headers = ["Ticker", "Action", "Token", "ADA", "Price", "Time"]
        for col_idx, header in enumerate(headers):
            trade_header_label = QLabel(header)
            trade_header_label.setStyleSheet(self.get_style(header_size, color, bold=True))
            trade_header_label.setAlignment(Qt.AlignCenter)
            self.trade_table.addWidget(trade_header_label, 0, col_idx)
        layout.addLayout(self.trade_table)
        layout.addSpacing(10)
        self.setLayout(layout)

    def _add_trade_row(self, trade, row_idx, font_size, color):
        
        now = datetime.now() 
        trade_time = datetime.fromtimestamp(trade.time)
        delta_time = (now - trade_time).total_seconds()

        if delta_time <= 60:
            time_ago = f"{delta_time:.0f}s ago"
        else:
            time_ago = f"{round(delta_time / 60)}m ago"

        labels = [
            trade.tokenAName,
            trade.action,
            f"{round(float(trade.tokenAAmount))}",
            f"{round(float(trade.tokenBAmount))}",
            f"{round(float(trade.price), 3)}",
            time_ago
        ]

        for col_idx, text in enumerate(labels):
            label = QLabel(str(text))
            label.setStyleSheet(self.get_style(font_size, color))
            self.trade_table.addWidget(label, row_idx, col_idx)

    def _clear_trade_rows(self):
        count = self.trade_table.count()
        header_count = self.trade_table.columnCount()
    
        for i in range(count - 1, header_count - 1, -1):
            item = self.trade_table.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
                self.trade_table.removeWidget(item.widget())

    def _remove_table_header(self, table):
        for col in range(table.columnCount()):
            item = table.itemAtPosition(0, col)
            if item and item.widget():
                widget = item.widget()
                widget.deleteLater()
                table.removeWidget(widget)

    def get_style(self, font_size=None, color=None, bold=False, header_size=False):
        font_size = font_size or self.config.get("font_size", 50)
        header_size = header_size or self.config.get("header_size", 20)
        color = color or self.config.get("color", "white")
        style = f"font-size: {font_size}px; color: {color};"
        if bold:
            style += f" {self.BOLD_STYLE}"
        return style

    def update_data(self):

        self._clear_trade_rows()

        font_size = self.config["font_size"]
        color = self.config["color"]
        trade_count = self.config["count"]
        ticker = self.config["ticker"]
        value = self.config["value"]

        token_id = TOKEN_ID_MAPPING.get(ticker)
        last_trades_data = get_last_token_trades("1h", token_id, value, "time", trade_count)

        last_trades = LastTrades(last_trades_data)

        if not last_trades.trades:
            self._remove_table_header(self.trade_table)
        else:
            row_idx = 1
            for trade in last_trades.trades:
                self._add_trade_row(trade, row_idx, font_size, color)
                row_idx += 1

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
