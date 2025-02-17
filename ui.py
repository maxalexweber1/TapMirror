import json
import os
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from api import get_token_by_id, get_market_stats, get_token_price_by_id,get_quote_price, get_token_holder, get_token_price_chg, get_token_trading_stats,get_portfolio_stats
from config import TOKEN_MAPPING, UPDATE_INTERVAL, PORTFOLIO_ADDRESS
from chart_widget import ChartWidget
from portfolio import Portfolio

# Load UI layout from JSON config file
def load_layout_config():
    with open("layout_config.json", "r") as file:
        return json.load(file)

class TapMirrorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.config = load_layout_config()
        self.ui_elements = {}  # store references to UI elements

        self.initUI()
        self.update_data()

        # Timer for automatic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(UPDATE_INTERVAL)

 # Sets up the UI dynamically based on the JSON configuration."""
    def initUI(self):
        self.setWindowTitle("TapMirror")
        self.setGeometry(0, 0, 800, 480)
        self.showFullScreen()

        layout = QGridLayout()
        layout.setSpacing(5)

# Start of Sections Loop
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

                    token_widgets[ticker] = {}

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
                        token_widgets[ticker]["image"] = image_label
                        

                    if "price" in show_options:
                        price_label = QLabel(f"{ticker}: Loading...")
                        price_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                        price_label.setAlignment(Qt.AlignVCenter)
                        token_hbox.addWidget(price_label)
                        token_widgets[ticker]["price"] = price_label

                    if "change"  in show_options:
                        change_label = QLabel(f"Loading...")
                        change_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                        change_label.setAlignment(Qt.AlignVCenter)
                        token_hbox.addWidget(change_label)
                        token_widgets[ticker]["change"] = change_label
                    
                    if "chart" in show_options:
                        chart_widget = None
                        chart_widget = ChartWidget(self)
                        chart_widget.setFixedSize(300, 150)
                    if chart_widget:
                        token_hbox.addWidget(chart_widget) 
                        token_widgets[ticker]["chart"] = chart_widget
                    
                    if "holders" in show_options:
                        holder_label = QLabel(f"Loading...")
                        holder_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                        holder_label.setAlignment(Qt.AlignVCenter)
                        token_hbox.addWidget(holder_label)
                        token_widgets[ticker]["holders"] = holder_label  
                    
                    if "buyvol"  in show_options:
                        buyvol_label = QLabel(f"Loading...")
                        buyvol_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                        buyvol_label.setAlignment(Qt.AlignVCenter)
                        token_hbox.addWidget(buyvol_label)
                        token_widgets[ticker]["buyvol"] = buyvol_label  
  
                    if "sellvol"  in show_options:
                        sellvol_label = QLabel(f"Loading...")
                        sellvol_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                        sellvol_label.setAlignment(Qt.AlignVCenter)   
                        token_hbox.addWidget(sellvol_label)
                        token_widgets[ticker]["sellvol"] = sellvol_label
                    token_vbox.addLayout(token_hbox)
                # saves token section
                self.ui_elements[f"tokens_{row}_{col}"] = token_widgets
                section_layout.addLayout(token_vbox)

            elif section["type"] == "clock":
                label = QLabel("Loading time...")
                label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                label.setAlignment(Qt.AlignCenter)
                self.ui_elements[f"clock_{row}_{col}"] = {"label": label}
                section_layout.addWidget(label)

            elif section["type"] == "market_data":
                quote_label = QLabel("")
                quote_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                quote_label.setAlignment(Qt.AlignCenter)
                self.ui_elements[f"quote_{row}_{col}"] = {"label": quote_label}
                section_layout.addWidget(quote_label)

                active_addr_label = QLabel("") 
                active_addr_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                active_addr_label.setAlignment(Qt.AlignCenter)
                self.ui_elements[f"activeAddresses_{row}_{col}"] = {"label": active_addr_label}
                section_layout.addWidget(active_addr_label)

                dex_vol_label = QLabel("") 
                dex_vol_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                dex_vol_label.setAlignment(Qt.AlignCenter)
                self.ui_elements[f"dexVolume_{row}_{col}"] = {"label": dex_vol_label}
                section_layout.addWidget(dex_vol_label)
            
            elif section["type"] == "portfolio":
                show_options = section.get("show", [])
                portfolio_vbox = QVBoxLayout()
                portfolio_widgets = {}

                if "adabalance" in show_options:
                   balance_label = QLabel(f"Loading...")
                   balance_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                   balance_label.setAlignment(Qt.AlignVCenter)
                   portfolio_vbox.addWidget(balance_label) 
                   portfolio_widgets["adabalance"] = balance_label

                if "adavalue"  in show_options:
                    value_label = QLabel(f"Loading...")
                    value_label.setStyleSheet(f"font-size: {section['font_size']}px; color: {section['color']};")
                    value_label.setAlignment(Qt.AlignVCenter)
                    portfolio_vbox.addWidget(value_label)     
                    portfolio_widgets["adavalue"] = value_label     
                    
                if "tokens" in show_options:
                    token_container_widget = QWidget()
                    token_container_layout = QVBoxLayout(token_container_widget)
                    portfolio_vbox.addWidget(token_container_widget)
                    portfolio_widgets["tokens"] = token_container_layout 
                    
                self.ui_elements[f"portfolio_{row}_{col}"] = portfolio_widgets
                section_layout.addLayout(portfolio_vbox)

            section_frame.setLayout(section_layout)
            layout.addWidget(section_frame, row, col)

        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
# Update screen Method 
    def update_data(self):
        """Fetches API data and updates the UI elements dynamically."""
        
        # Update token data
        for key, token_widgets in self.ui_elements.items():
            if key.startswith("tokens"):
                for ticker, elements in token_widgets.items():
                    price_label = elements.get("price")
                    chart_widget = elements.get("chart")
                    holder_label = elements.get("holders")
                    change_label = elements.get("change")
                    buyvol_label = elements.get("buyvol")
                    sellvol_label = elements.get("sellvol")

                    token_id = TOKEN_MAPPING.get(ticker)
                    # Price
                    if price_label and token_id:
                        token_data = get_token_by_id(token_id)
                        if token_data:
                            price = round(float(token_data.get("price", 0)), 4)
                            price_label.setText(f"{ticker}: {price} ₳")
                    # Chart         
                    if chart_widget:
                        price_data = get_token_price_by_id(token_id, "1D", 7)
                        chart_widget.update_chart(price_data)
                    # Token holder
                    if holder_label:
                        holder_data = get_token_holder(token_id)
                        if holder_data:
                            holders = holder_data.get("holders")
                            holder_label.setText(f"Holder: {holders}")
                    # Token Changes            
                    if change_label:
                        change_data = get_token_price_chg(token_id, "1h", "4h", "24h")
                        ch_1 = round(float(change_data.get("1h")) * 100, 2)
                        ch_2 = round(float(change_data.get("4h")) * 100, 2)
                        ch_3 = round(float(change_data.get("24h")) * 100, 2)
                        change_label.setText(f"1h: {ch_1}% 4h: {ch_2}% 24h: {ch_3}%")
                    if buyvol_label or sellvol_label:
                        trade_data = get_token_trading_stats(token_id,"24h")
                        if buyvol_label:
                            buyvol_label.setText(f"Buy Vol: { trade_data.get("buyVolume")}")
                        if sellvol_label:
                            sellvol_label.setText(f"Sell Vol: { trade_data.get("sellVolume")}")    
                        
        # Update clock
        for key, elements in self.ui_elements.items():
            if key.startswith("clock"):
                label = elements.get("label")
                if label:
                    label.setText(datetime.now().strftime("%H:%M:%S"))

        # Update market data
        market_data = get_market_stats("ADA")
        for key, elements in self.ui_elements.items():
            if key.startswith("activeAddresses") and market_data:
                active_addr_label = elements.get("label")
                active_addr   = market_data.get("activeAddresses")
                active_addr_label.setText(f"Active Addr: {active_addr}")
            if key.startswith("dexVolume") and market_data:
                dex_vol_label = elements.get("label")
                dex_vol   = market_data.get("dexVolume")
                dex_vol_f = float(dex_vol)
                dex_vol_millions = dex_vol_f / 1_000_000
                dex_vol_label.setText(f"Dex Vol: {dex_vol_millions:.2f} Mio ADA")

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

        # Update portfolio Data
        portfolio_response = get_portfolio_stats(PORTFOLIO_ADDRESS)
        portfolio = Portfolio(portfolio_response)
        for key, elements in self.ui_elements.items():
            if key.startswith("portfolio") and portfolio:
        # Hier gehst du explizit die Labels in elements durch:
                if "adabalance" in elements:
                    balance_label = elements["adabalance"]
                    ada_balance  = round(float(portfolio.ada_balance))
                    balance_label.setText(f"Balance: {ada_balance} ₳")
                if "adavalue" in elements:
                    value_label = elements["adavalue"]
                    ada_value  = round(float(portfolio.ada_value))
                    value_label.setText(f"Portfolio Value: {ada_value} ₳")
                if "tokens" in elements:
                    token_container = elements["tokens"]
                    
                    while token_container.count():
                        item = token_container.takeAt(0)
                        widget = item.widget()
                        if widget is not None:
                            widget.deleteLater()

                    # Header: Number of Tokens
                    token_count = len(portfolio.positions_ft)
                    header_label = QLabel(f"Token: {token_count}")
                    header_label.setStyleSheet("color: white; font-size: 16px;")
                    token_container.addWidget(header_label)

                    # For every Token in Portfolio
                    for token in portfolio.positions_ft:
                      if token.ticker != 'ADA':
                        row_layout = QHBoxLayout()
                        # Logo
                        logo_label = QLabel()
                        image_path = f"assets/{token.ticker}.png"
                        if os.path.exists(image_path):
                            pixmap = QPixmap(image_path).scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            logo_label.setPixmap(pixmap)
                        else:
                            logo_label.setText("[No Image]")
                        logo_label.setFixedSize(70, 70)
                        row_layout.addWidget(logo_label)

                        # Ticker
                        ticker_label = QLabel(token.ticker)
                        ticker_label.setStyleSheet("color: white; font-size: 16px;")
                        row_layout.addWidget(ticker_label)

                        if token.price:
                         price = round(float(token.price), 4)
                         price_label = QLabel(f"{price} ₳")
                         price_label.setStyleSheet("color: white; font-size: 16px;")
                         row_layout.addWidget(price_label)

                        token_container.addLayout(row_layout)
# Exit Application
    def keyPressEvent(self, event):
        """Allows the ESC key to exit the application."""
        if event.key() == Qt.Key_Escape:
            self.close()  # Closes the application
