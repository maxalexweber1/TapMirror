import json
from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from widgets.token_widget import TokenWidget
from widgets.clock_widget import ClockWidget
from widgets.market_data_widget import MarketDataWidget
from widgets.portfolio_widget import PortfolioWidget
from api.api import get_portfolio_stats
from config.config import PORTFOLIO_ADDRESS
from portfolio import Portfolio

def load_layout_config():
    with open("./config/layout_config.json", "r") as file:
        return json.load(file)

class TapMirrorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.config = load_layout_config()
        self.ui_elements = {}
        self.portfolio_data = None

        self.initUI()
        self.update_data()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(10000)

    def initUI(self):
        self.setWindowTitle("TapMirror")
        self.setGeometry(0, 0, 800, 480)
        self.showFullScreen()

        layout = QGridLayout()
        layout.setSpacing(5)

        for section in self.config["sections"]:
            row, col = section["position"]
            print(f"Creating widget for {section['type']} at position [{row}, {col}]")  # Debug
            section_frame = QFrame()
            section_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
            section_frame.setStyleSheet("border: 1px solid gray; border-radius: 5px; background-color: #333;")

            if section["type"] == "tokens":
                widget = TokenWidget(section)
                self.ui_elements[f"tokens_{row}_{col}"] = widget
            elif section["type"] == "clock":
                widget = ClockWidget(section)
                self.ui_elements[f"clock_{row}_{col}"] = widget
            elif section["type"] == "market_data":
                widget = MarketDataWidget(section)
                self.ui_elements[f"market_data_{row}_{col}"] = widget
            elif section["type"] == "portfolio":
                widget = PortfolioWidget(section, self.portfolio_data)
                self.ui_elements[f"portfolio_{row}_{col}"] = widget

            section_frame.setLayout(widget.layout())
            layout.addWidget(section_frame, row, col)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #1a1a1a;")

    def update_data(self):
        portfolio_response = get_portfolio_stats(PORTFOLIO_ADDRESS)
        self.portfolio_data = Portfolio(portfolio_response)

        for key, widget in self.ui_elements.items():
            print(f"Updating widget: {key}")  # Debug
            if key.startswith("portfolio"):
                widget.update_data(self.portfolio_data)
            else:
                widget.update_data()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()