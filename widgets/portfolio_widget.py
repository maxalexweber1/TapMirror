from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
from datetime import datetime
from api.api import get_portfolio_stats, get_portfolio_trade_history
from config.config import PORTFOLIO_ADDRESS

class PortfolioWidget(QWidget):
    HEADER_FONT_SIZE = 25  # TODO put into config file
    BOLD_STYLE = "font-weight: bold;"  # TODO put into config file

    def __init__(self, config):
        super().__init__()
        self.config = config  
        self.initUI()

    def get_style(self, font_size=None, color=None, bold=False):
        """Helper function to generate consistent stylesheets from config."""
        font_size = font_size or self.config["font_size"] 
        color = color or self.config["color"] 
        style = f"font-size: {font_size}px; color: {color};"
        if bold:
            style += f" {self.BOLD_STYLE}"
        return style

    def initUI(self):
        """Initialize the UI layout and widgets based on config."""
        layout = QVBoxLayout()

        # Extract style attributes from config
        font_size = self.config["font_size"]
        color = self.config["color"]
        inner_widgets = self.config["innerWidgets"]

        # Add ADA balance label if specified in innerWidgets
        if "adabalance" in inner_widgets:
            self.balance_label = QLabel("Loading...")
            self.balance_label.setStyleSheet(self.get_style())
            self.balance_label.setAlignment(Qt.AlignVCenter)
            layout.addWidget(self.balance_label)

        # Add portfolio value label if specified in innerWidgets
        if "adavalue" in inner_widgets:
            self.value_label = QLabel("Loading...")
            self.value_label.setStyleSheet(self.get_style())
            self.value_label.setAlignment(Qt.AlignVCenter)
            layout.addWidget(self.value_label)

        # Add token table if specified in innerWidgets
        if "tokens" in inner_widgets:
            self.token_table = QGridLayout()
            headers = ["Token", "Ticker", "Price", "Holdings", "Value", "24h", "7d", "30d"]
            for col_idx, header in enumerate(headers):
                token_header_label = QLabel(header)
                token_header_label.setStyleSheet(self.get_style(self.HEADER_FONT_SIZE, color, bold=True))
                token_header_label.setAlignment(Qt.AlignCenter)
                self.token_table.addWidget(token_header_label, 0, col_idx)
            layout.addLayout(self.token_table)
            layout.addSpacing(10) 

        # Add liquidity pool positions table if specified in innerWidgets
        if "lppos" in inner_widgets:
            self.lppos_table = QGridLayout()
            headers = ["LP Token", "Amount LP", "TokenA/TokenB", "Value"]
            for col_idx, header in enumerate(headers):
                lp_header_label = QLabel(header)
                lp_header_label.setStyleSheet(self.get_style(self.HEADER_FONT_SIZE, color, bold=True))
                lp_header_label.setAlignment(Qt.AlignCenter)
                self.lppos_table.addWidget(lp_header_label, 0, col_idx)
            layout.addLayout(self.lppos_table)
            layout.addSpacing(10) 

        # Add NFT table if specified in innerWidgets
        if "nfts" in inner_widgets:
            self.nft_table = QGridLayout()
            headers = ["Name", "Amount", "Value", "24h", "7d", "30d"]
            for col_idx, header in enumerate(headers):
                nft_header_label = QLabel(header)
                nft_header_label.setStyleSheet(self.get_style(self.HEADER_FONT_SIZE, color, bold=True))
                nft_header_label.setAlignment(Qt.AlignCenter)
                self.nft_table.addWidget(nft_header_label, 0, col_idx)
            layout.addLayout(self.nft_table)
            layout.addSpacing(10) 
        # Add trade table if specified in innerWidgets
        if "trades" in inner_widgets:
            self.trade_table = QGridLayout()
            headers = ["Action", "Time", "Token", "Amount", "ADA", "Change"]
            for col_idx, header in enumerate(headers):
                trade_header_label = QLabel(header)
                trade_header_label.setStyleSheet(self.get_style(self.HEADER_FONT_SIZE, color, bold=True))
                trade_header_label.setAlignment(Qt.AlignCenter)
                self.trade_table.addWidget(trade_header_label, 0, col_idx)
            layout.addLayout(self.trade_table)

        self.setLayout(layout)

    def update_data(self):
        """Update widget data from portfolio API."""
        portfolio_data = get_portfolio_stats(PORTFOLIO_ADDRESS)
        portfolio_trades = get_portfolio_trade_history(PORTFOLIO_ADDRESS)
        portfolio = Portfolio(portfolio_data)
        trades = PortfolioTrades(portfolio_trades)

        # Retrieve style attributes from config
        font_size = self.config["font_size"]
        color = self.config["color"]

        # Update ADA balance
        if hasattr(self, "balance_label"):
            ada_balance = round(float(portfolio.ada_balance))
            self.balance_label.setText(f"ADA: {ada_balance} ₳")

        # Update portfolio value
        if hasattr(self, "value_label"):
            ada_value = round(float(portfolio.ada_value))
            self.value_label.setText(f"Portfolio Value: {ada_value} ₳")

        # Update token table
        if hasattr(self, "token_table"):
            self._clear_table(self.token_table)
            row_idx = 1
            for token in portfolio.positions_ft:
                if token.ticker == 'ADA':
                    continue
                self._add_token_row(token, row_idx, font_size, color)
                row_idx += 1

        # Update liquidity pool positions table
        if hasattr(self, "lppos_table"):
            self._clear_table(self.lppos_table)
            if not portfolio.positions_lp:
                self._remove_table_header(self.lppos_table)
            else:        
                row_idx = 1
                for lp_pos in portfolio.positions_lp:
                    self._add_lppos_row(lp_pos, row_idx, font_size, color)
                    row_idx += 1

        # Update NFT table
        if hasattr(self, "nft_table"):
            self._clear_table(self.nft_table)
            row_idx = 1
            for nft in portfolio.positions_nft:
                self._add_nft_row(nft, row_idx, font_size, color)
                row_idx += 1

        # Update trade table
        if hasattr(self, "trade_table"):
            self._clear_table(self.trade_table)
            row_idx = 1
            for trade in trades.trades:
                if row_idx <= 5:
                    self._add_trade_row(trade, row_idx, font_size, color)
                row_idx += 1

    def _clear_table(self, table):
        """Helper function to clear table contents."""
        for i in range(table.rowCount() - 1, 0, -1):
            for j in range(table.columnCount()):
                item = table.itemAtPosition(i, j)
                if item and item.widget():
                    widget = item.widget()
                    widget.deleteLater()
                    table.removeWidget(widget)

    def _add_token_row(self, token, row_idx, font_size, color):
        """Add a row to the token table."""
        image_label = QLabel()
        image_path = os.path.join("assets", f"{token.ticker}.png")
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.black)
        if os.path.exists(image_path):
            temp_pixmap = QPixmap(image_path)
            if not temp_pixmap.isNull():
                pixmap = temp_pixmap
        pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        self.token_table.addWidget(image_label, row_idx, 0)

        labels = [
            (token.ticker, 1),
            (f"{round(float(token.price), 3)} ₳" if token.price else "N/A", 2),
            (str(round(float(token.balance))) if token.balance else "N/A", 3),
            (f"{round(float(token.ada_value))} ₳" if token.ada_value else "N/A", 4),
            (f"{round(float(token.change_24h) * 100, 2)}%" if token.change_24h else "N/A", 5),
            (f"{round(float(token.change_7d) * 100, 2)}%" if token.change_7d else "N/A", 6),
            (f"{round(float(token.change_30d) * 100, 2)}%" if token.change_30d else "N/A", 7),
        ]
        for text, col_idx in labels:
            label = QLabel(text)
            label.setStyleSheet(self.get_style(font_size, color))
            self.token_table.addWidget(label, row_idx, col_idx)

    def _add_lppos_row(self, lp_pos, row_idx, font_size, color):
        """Add a row to the liquidity pool positions table."""
        labels = [
            (lp_pos.ticker, 0),
            (f"{round(float(lp_pos.amount_lp), 3)}" if lp_pos.amount_lp else "N/A", 1),
            (f"{round(float(lp_pos.token_a_amount))}" if lp_pos.token_a_amount else "N/A", 2),
            (f"{round(float(lp_pos.token_b_amount))}" if lp_pos.token_b_amount else "N/A", 3),
            (f"{round(float(lp_pos.ada_value))} ₳" if lp_pos.ada_value else "N/A", 4),
        ]
        for text, col_idx in labels:
            label = QLabel(text)
            label.setStyleSheet(self.get_style(font_size, color))
            self.lppos_table.addWidget(label, row_idx, col_idx)

    def _add_nft_row(self, nft, row_idx, font_size, color):
        """Add a row to the NFT table."""
        labels = [
            (nft.name, 0),
            (str(round(float(nft.balance))) if nft.balance else "N/A", 1),
            (f"{round(float(nft.ada_value))} ₳" if nft.ada_value else "N/A", 2),
            (f"{round(float(nft.change_24h) * 100, 2)}%" if nft.change_24h else "N/A", 3),
            (f"{round(float(nft.change_7d) * 100, 2)}%" if nft.change_7d else "N/A", 4),
            (f"{round(float(nft.change_30d) * 100, 2)}%" if nft.change_30d else "N/A", 5),
        ]
        for text, col_idx in labels:
            label = QLabel(text)
            label.setStyleSheet(self.get_style(font_size, color))
            self.nft_table.addWidget(label, row_idx, col_idx)

    def _add_trade_row(self, trade, row_idx, font_size, color):
        """Add a row to the trade table."""
        formatted_time = datetime.fromtimestamp(float(trade.time)).strftime("%d-%m-%y %H:%M:%S")
        labels = [
            (trade.action, 0),
            (formatted_time, 1),
            (trade.tokenAName, 2),
            (f"{round(float(trade.tokenAAmount), 3)}" if trade.tokenAAmount else "N/A", 3),
            (f"{round(float(trade.tokenBAmount), 3)}" if trade.tokenBAmount else "N/A", 4),
            ("N/A", 5),  # TODO need to calculate change since trade 
        ]
        for text, col_idx in labels:
            label = QLabel(str(text))
            label.setStyleSheet(self.get_style(font_size, color))
            self.trade_table.addWidget(label, row_idx, col_idx)

    def _remove_table_header(self, table):
        """Removes header from a emty table"""
        for col in range(table.columnCount()):
            item = table.itemAtPosition(0, col)
            if item and item.widget():
                widget = item.widget()
                widget.deleteLater()
                table.removeWidget(widget)

class Portfolio:
    def __init__(self, data):
        self.ada_balance = data.get("adaBalance")
        self.ada_value = data.get("adaValue")
        self.liquid_value = data.get("liquidValue")
        self.num_FTs = data.get("numFTs")
        self.num_NFTs = data.get("numNFTs")
        self.positions_ft = [PositionFt(ft) for ft in data.get("positionsFt", [])]
        self.positions_lp = [PositionLp(lp) for lp in data.get("positionsLp", [])]
        self.positions_nft = [PositionNft(nft) for nft in data.get("positionsNft", [])]

class PositionLp:
    def __init__(self, data):
        self.ada_value = data.get("adaValue")
        self.amount_lp = data.get("amountLP")
        self.exchange = data.get("exchange")
        self.ticker = data.get("ticker")
        self.token_a = data.get("tokenA")
        self.token_a_amount = data.get("tokenAAmount")
        self.token_a_name = data.get("tokenAName")
        self.token_b = data.get("tokenB")
        self.token_b_amount = data.get("tokenBAmount")
        self.token_b_name = data.get("tokenBName")
        self.unit = data.get("unit")


class PositionNft:
    def __init__(self, data):
        self.change_24h = data.get("24h")
        self.change_30d = data.get("30d")
        self.change_7d = data.get("7d")
        self.ada_value = data.get("adaValue")
        self.balance = data.get("balance")
        self.floor_price = data.get("floorPrice")
        self.liquid_value = data.get("liquidValue")
        self.listings = data.get("listings")
        self.name = data.get("name")
        self.policy = data.get("policy")


class PositionFt:
    def __init__(self, data):
        self.change_24h = data.get("24h")
        self.change_30d = data.get("30d")
        self.change_7d = data.get("7d")
        self.ada_value = data.get("adaValue")
        self.balance = data.get("balance")
        self.fingerprint = data.get("fingerprint")
        self.liquidBalance = data.get("liquidBalance")
        self.liqidValue = data.get("liquidValue")
        self.price = data.get("price")
        self.ticker = data.get("ticker")
        self.unit = data.get("unit")

class PortfolioTrades:
    def __init__(self, data):        
        self.trades = [Trade(tr) for tr in data]

class Trade:
    def __init__(self, data):        
        self.action = data.get("action")
        self.time = data.get("time")
        self.tokenAName = data.get("tokenAName")
        self.tokenAAmount = data.get("tokenAAmount")
        self.tokenBName = data.get("tokenBName")
        self.tokenBAmount = data.get("tokenBAmount")

