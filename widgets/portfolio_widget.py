from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtGui import QPixmap
import os
from PyQt5.QtWidgets import QSizePolicy
from datetime import datetime
from widgets.portfolio_chart_widget import PortfolioChartWidget 
from api.taptools_api import get_portfolio_stats, get_portfolio_trade_history, get_portfolio_trended_value, get_token_by_id
from widgets.style_manager import StyleManager 

class PortfolioWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config  
        self.style_manager = StyleManager()
        self.initUI()
        self.update_data()

        refresh = self.config.get("refresh", 100000)
        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(refresh)

    def initUI(self):
        """Initialize the UI layout and widgets based on config."""
        layout = QVBoxLayout()
        color = self.style_manager.get_style("portfolio", "color", "white")
        font_size = self.style_manager.get_scaled_font_size(self.config)
        header_size = self.style_manager.get_scaled_header_size(self.config)
        inner_widgets = self.config["innerWidgets"]
        chart_l, chart_h = self.config["chart_size"]
        spacing_size = 30

        if any(widget in inner_widgets for widget in ["adabalance", "adavalue", "chart"]):
            top_labels_layout = QHBoxLayout()

            if "adabalance" in inner_widgets:
                self.balance_label = QLabel("Loading...")
                self.balance_label.setStyleSheet(self.get_style(header_size, color, bold=True))
                self.balance_label.setAlignment(Qt.AlignCenter)
                top_labels_layout.addWidget(self.balance_label)

            if "adavalue" in inner_widgets:
                self.value_label = QLabel("Loading...")
                self.value_label.setStyleSheet(self.get_style(header_size, color, bold=True))
                self.value_label.setAlignment(Qt.AlignCenter)
                top_labels_layout.addWidget(self.value_label)

            if "chart" in inner_widgets:
                self.chart_widget = PortfolioChartWidget(self)
                self.chart_widget.setFixedSize(chart_l, chart_h)
                top_labels_layout.addWidget(self.chart_widget)

            layout.addLayout(top_labels_layout)
            layout.addSpacing(spacing_size)

        if "tokens" in inner_widgets:
            self.token_table = QGridLayout()
            headers = ["Tokens"]
            for col_idx, header in enumerate(headers):
                token_header_label = QLabel(header)
                token_header_label.setStyleSheet(self.get_style(font_size, color, bold=True))
                token_header_label.setAlignment(Qt.AlignCenter)
                self.token_table.addWidget(token_header_label, 0, col_idx)
            layout.addLayout(self.token_table)
            layout.setSizeConstraint(QGridLayout.SetMinimumSize)
            layout.addSpacing(spacing_size)  

        if "lppos" in inner_widgets:
            self.lppos_table = QGridLayout()
            headers = ["LP Positions"]
            for col_idx, header in enumerate(headers):
                lp_header_label = QLabel(header)
                lp_header_label.setStyleSheet(self.get_style(font_size, color, bold=True))
                lp_header_label.setAlignment(Qt.AlignCenter)
                self.lppos_table.addWidget(lp_header_label, 0, col_idx)
            layout.addLayout(self.lppos_table)
            layout.addSpacing(spacing_size)  

        if "nfts" in inner_widgets:
            self.nft_table = QGridLayout()
            headers = ["NFTs"]
            for col_idx, header in enumerate(headers):
                nft_header_label = QLabel(header)
                nft_header_label.setStyleSheet(self.get_style(font_size, color, bold=True))
                nft_header_label.setAlignment(Qt.AlignCenter)
                self.nft_table.addWidget(nft_header_label, 0, col_idx)
            layout.addLayout(self.nft_table)
            layout.addSpacing(spacing_size)  

        if "trades" in inner_widgets:
            self.trade_table = QGridLayout()
            headers = ["Last Trades"]
            for col_idx, header in enumerate(headers):
                trade_header_label = QLabel(header)
                trade_header_label.setStyleSheet(self.get_style(font_size, color, bold=True))
                trade_header_label.setAlignment(Qt.AlignCenter)
                self.trade_table.addWidget(trade_header_label, 0, col_idx)
            layout.addLayout(self.trade_table)

        layout.addStretch(1)

        self.setLayout(layout)


    def update_data(self):
        """Update widget data from portfolio API."""
        address = self.config["address"]
        portfolio_data = get_portfolio_stats(address)
        portfolio_trades = get_portfolio_trade_history(address)
        portfolio_value = get_portfolio_trended_value(address,"30d","ADA")
        portfolio = Portfolio(portfolio_data)
        trades = PortfolioTrades(portfolio_trades)

        font_size = self.style_manager.get_scaled_font_size("portfolio")
    
        color = self.style_manager.get_style("portfolio", "color", "white")

        if hasattr(self, "balance_label"):
            ada_balance = round(float(portfolio.ada_balance))
            self.balance_label.setText(f" ADA: {ada_balance} ₳ ")

        if hasattr(self, "value_label"):
            ada_value = round(float(portfolio.ada_value))
            self.value_label.setText(f" Portfolio Value: {ada_value} ₳ ")

        if hasattr(self,"chart_widget"):
             self.chart_widget.update_chart(portfolio_value) 

        if hasattr(self, "token_table"):
            self._clear_table(self.token_table)
            if not portfolio.positions_ft:
                self._remove_table_header(self.token_table)
            else:    
                row_idx = 1
                for token in portfolio.positions_ft:
                    if row_idx <= 5:
                        if token.ticker == 'ADA':
                            continue
                        self._add_token_row(token, row_idx, font_size, color)
                        row_idx += 1

        if hasattr(self, "lppos_table"):
            self._clear_table(self.lppos_table)
            if not portfolio.positions_lp:
                self._remove_table_header(self.lppos_table)
            else:        
                row_idx = 1
                for lp_pos in portfolio.positions_lp:
                    self._add_lppos_row(lp_pos, row_idx, font_size, color)
                    row_idx += 1

        if hasattr(self, "nft_table"):
            self._clear_table(self.nft_table)
            if not portfolio.positions_nft:
                self._remove_table_header(self.lppos_table)
            else:
                row_idx = 1
                for nft in portfolio.positions_nft:
                    self._add_nft_row(nft, row_idx, font_size, color)
                    row_idx += 1

        if hasattr(self, "trade_table"):
            self._clear_table(self.trade_table)
            if not trades.trades:
                self._remove_table_header(self.trade_table)
            else:    
                row_idx = 1
                for trade in trades.trades:
                    if row_idx <= 5:
                        self._add_trade_row(trade, row_idx, font_size, color)
                    row_idx += 1
        self.adjustSize()

    def _clear_table(self, table):
        """clear table contents."""
        for i in range(table.rowCount() - 1, 0, -1):
            for j in range(table.columnCount()):
                item = table.itemAtPosition(i, j)
                if item and item.widget():
                    widget = item.widget()
                    widget.deleteLater()
                    table.removeWidget(widget)

    def _add_token_row(self, token, row_idx, font_size, color):
        """Add a row to the token table."""
        image_scale = self.style_manager.get_scaled_value("portfolio", "image_size", 60)
        image_label = QLabel()
        image_path = os.path.join("assets/token", f"{token.ticker}.png")
        pixmap = QPixmap(image_scale , image_scale )
        pixmap.fill(Qt.black)
        if os.path.exists(image_path):
            temp_pixmap = QPixmap(image_path)
            if not temp_pixmap.isNull():
                pixmap = temp_pixmap
        pixmap = pixmap.scaled(image_scale, image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        self.token_table.addWidget(image_label, row_idx, 0)

        labels = [
            (f"{token.ticker}<br>"  
             f"{round(float(token.price), 3)} ₳", 1), 
            (f"{round(float(token.ada_value))} ₳ <br>"
             f"{StyleManager.format_number(round(float(token.balance)))} {token.ticker}", 2),
            (f"24h: {round(float(token.change_24h) * 100, 2)}%" if token.change_24h else "0 %", 3),
            (f"7d: {round(float(token.change_7d) * 100, 2)}%" if token.change_7d else "0 %" , 4),
            (f"30d: {round(float(token.change_30d) * 100, 2)}%" if token.change_30d else "0 %", 5),
        ]
        for text, col_idx in labels:
            label = QLabel(text)
            label.setWordWrap(True)
            label.setStyleSheet(self.get_style(font_size, color))
            self.token_table.addWidget(label, row_idx, col_idx)

    def _add_lppos_row(self, lp_pos, row_idx, font_size, color):
        """Add a row to the liquidity pool positions table."""
        labels = [
            (lp_pos.ticker, 0),
            (f"{round(float(lp_pos.token_a_amount))} { (str(lp_pos.ticker)).split("/")[0].strip()}/ <br>"  
             f"{round(float(lp_pos.token_b_amount))} ₳", 1 ), 
            (f"Value: {round(float(lp_pos.ada_value))} ₳" if lp_pos.ada_value else "N/A", 2),
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

        token_data = get_token_by_id(trade.tokenA)

        if token_data:
            price_now = float(token_data.get("price", 0))
            trade_price = float(trade.tokenBAmount) / float(trade.tokenAAmount)
            
            change = round(100- (trade_price / price_now) * 100,2)

            action_color = "green" if trade.action.lower() == "buy" else "red" if trade.action.lower() == "sell" else "yellow"


        labels = [
            (trade.action, 0, action_color),
            (formatted_time, 1),
            (trade.tokenAName, 2),
            (f"{round(float(trade.tokenAAmount))}" if trade.tokenAAmount else "N/A", 3),
            (f"{round(float(trade.tokenBAmount))}" if trade.tokenBAmount else "N/A", 4),
            (f"{change} %", 5), 
        ]
        for label_data in labels:
            text = label_data[0]
            col_idx = label_data[1]
            label_color = label_data[2] if len(label_data) > 2 else color
            label = QLabel(str(text))
            label.setStyleSheet(f"font-size: {font_size}px; color: {label_color};")
            self.trade_table.addWidget(label, row_idx, col_idx)

    def _remove_table_header(self, table):
        """Removes header from a emty table"""
        for col in range(table.columnCount()):
            item = table.itemAtPosition(0, col)
            if item and item.widget():
                widget = item.widget()
                widget.deleteLater()
                table.removeWidget(widget)

    def get_style(self, font_size=None, color=None, bold=False):
        """generate consistent stylesheets from config."""
        style = f"font-size: {font_size}px; color: {color};"
        if bold:
            style += f"font-weight: bold;"
        return style

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
        self.tokenA = data.get("tokenA")
        self.tokenAName = data.get("tokenAName")
        self.tokenAAmount = data.get("tokenAAmount")
        self.tokenBName = data.get("tokenBName")
        self.tokenBAmount = data.get("tokenBAmount")
