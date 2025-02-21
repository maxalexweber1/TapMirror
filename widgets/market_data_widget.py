from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from api.api import get_market_stats, get_quote_price

class MarketDataWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.market_elements = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        inner_widgets = self.config.get("innerWidgets", [])
        font_size = self.config.get("font_size", 50)
        color = self.config.get("color", "white")
        style = f"font-size: {font_size}px; color: {color};"

        if "quote" in inner_widgets:
            quote_label = QLabel("Loading...")
            quote_label.setStyleSheet(style)
            quote_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(quote_label)
            self.market_elements["quote"] = quote_label

        if "activeaddresses" in inner_widgets:
            active_addr_label = QLabel("Loading...")
            active_addr_label.setStyleSheet(style)
            active_addr_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(active_addr_label)
            self.market_elements["activeaddresses"] = active_addr_label

        if "dexvolume" in inner_widgets:
            dex_vol_label = QLabel("Loading...")
            dex_vol_label.setStyleSheet(style)
            dex_vol_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(dex_vol_label)
            self.market_elements["dexvolume"] = dex_vol_label

        self.setLayout(layout)

    def update_data(self, data=None):
        market_data = get_market_stats("ADA")
        if "quote" in self.market_elements:
            quote_data = get_quote_price("USD")
            if quote_data and "price" in quote_data:
                price = round(float(quote_data["price"]), 4)
                self.market_elements["quote"].setText(f"ADA Price: {price} $")
            else:
                self.market_elements["quote"].setText("ADA Price: N/A")
        if "activeaddresses" in self.market_elements and market_data:
            active_addr = market_data.get("activeAddresses")
            self.market_elements["activeaddresses"].setText(f"Active Addr: {active_addr}")
        if "dexvolume" in self.market_elements and market_data:
            dex_vol = market_data.get("dexVolume")
            dex_vol_f = float(dex_vol)
            dex_vol_millions = dex_vol_f / 1_000_000
            self.market_elements["dexvolume"].setText(f"Dex Vol: {dex_vol_millions:.2f} Mio ADA")