from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt, QTimer
from api.taptools_api import get_market_stats, get_quote_price
from widgets.style_manager import StyleManager

class MarketDataWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.style_manager = StyleManager()
        self.market_elements = {}
        self.initUI()

        refresh = self.config.get("refresh", 100000)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(refresh)
        self.update_data()

    def initUI(self):
        layout = QHBoxLayout()
        font_size = self.style_manager.get_scaled_font_size("market_data")
        color = self.style_manager.get_style("market_data", "color", "white")
        frame_style = "border: 1px solid gray; border-radius: 5px;"
        
        inner_widgets = self.config.get("innerWidgets", [])
        
        if "quote" in inner_widgets:
            quote_frame = QFrame()
            quote_frame.setStyleSheet(frame_style)
            quote_layout = QHBoxLayout()
            quote_layout.setContentsMargins(5, 5, 5, 5)
            quote_label = QLabel("Loading...")
            quote_label.setStyleSheet(f"font-size: {font_size}px; color: {color}; border: none;")
            quote_label.setAlignment(Qt.AlignCenter)
            quote_layout.addWidget(quote_label)
            quote_frame.setLayout(quote_layout)
            layout.addWidget(quote_frame)
            self.market_elements["quote"] = quote_label
            layout.addSpacing(15) 
            
        if "activeaddresses" in inner_widgets:
            active_addr_frame = QFrame()
            active_addr_frame.setStyleSheet(frame_style)
            active_addr_layout = QHBoxLayout()
            active_addr_layout.setContentsMargins(5, 5, 5, 5) 
            active_addr_label = QLabel("Loading...")
            active_addr_label.setStyleSheet(f"font-size: {font_size}px; color: {color}; border: none;")
            active_addr_label.setAlignment(Qt.AlignCenter)
            active_addr_layout.addWidget(active_addr_label)
            active_addr_frame.setLayout(active_addr_layout)
            layout.addWidget(active_addr_frame)
            self.market_elements["activeaddresses"] = active_addr_label
            layout.addSpacing(15)  

        if "dexvolume" in inner_widgets:
            dex_vol_frame = QFrame()
            dex_vol_frame.setStyleSheet(frame_style)
            dex_vol_layout = QHBoxLayout()
            dex_vol_layout.setContentsMargins(5, 5, 5, 5)  
            dex_vol_label = QLabel("Loading...")
            dex_vol_label.setStyleSheet(f"font-size: {font_size}px; color: {color}; border: none;")
            dex_vol_label.setAlignment(Qt.AlignCenter)
            dex_vol_layout.addWidget(dex_vol_label)
            dex_vol_frame.setLayout(dex_vol_layout)
            layout.addWidget(dex_vol_frame)
            self.market_elements["dexvolume"] = dex_vol_label
         
        layout.setContentsMargins(0, 0, 0, 0)  
        self.setLayout(layout)

    def update_data(self):
        market_data = get_market_stats("ADA")
        if "quote" in self.market_elements:
            quote_data = get_quote_price("USD")
            if quote_data and "price" in quote_data:
                price = round(float(quote_data["price"]), 4)
                self.market_elements["quote"].setText(f"ADA Price: {price} $")
            else:
                self.market_elements["quote"].setText("ADA Price: N/A")
        
        if "activeaddresses" in self.market_elements and market_data:
            active_addr = market_data.get("activeAddresses", "N/A")
            self.market_elements["activeaddresses"].setText(f"Active Addr: {active_addr}")
        
        if "dexvolume" in self.market_elements and market_data:
            dex_vol = market_data.get("dexVolume", 0)
            dex_vol_millions = float(dex_vol) / 1_000_000
            self.market_elements["dexvolume"].setText(f"Dex Vol: {dex_vol_millions:.2f} Mio ADA")