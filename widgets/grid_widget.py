
from PyQt5.QtWidgets import QWidget, QGridLayout, QFrame, QVBoxLayout
from widgets.token_widget import TokenWidget
from widgets.clock_widget import ClockWidget
from widgets.market_data_widget import MarketDataWidget
from widgets.portfolio_widget import PortfolioWidget
from widgets.token_trades_widget import TokenTradesWidget
from widgets.weather_widget import WeatherWidget
from widgets.token_loans_widget import TokenLoansWidget

class GridWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.ui_elements = {}
        self.initUI()
        self.update_data()

    def initUI(self):
        layout = QGridLayout()
        layout.setSpacing(5)

        for section in self.config:
            row, col = section["position"]
            section_frame = QFrame()
            section_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
            section_frame.setStyleSheet(
                "border: 1px solid gray; border-radius: 5px; background-color: #000000;"
            )

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
                widget = PortfolioWidget(section)
                self.ui_elements[f"portfolio_{row}_{col}"] = widget
            elif section["type"] == "lasttrades":
                widget = TokenTradesWidget(section)
                self.ui_elements[f"trades_{row}_{col}"] = widget
            elif section["type"] == "weather":
                widget = WeatherWidget(section)
                self.ui_elements[f"weather_{row}_{col}"] = widget
            elif section["type"] == "exploans":
                widget = TokenLoansWidget(section)
                self.ui_elements[f"exploans_{row}_{col}"] = widget

            frame_layout = QVBoxLayout()
            frame_layout.addWidget(widget)
            section_frame.setLayout(frame_layout)

            layout.addWidget(section_frame, row, col)
            layout.setRowStretch(row, 1)
            layout.setColumnStretch(col, 1)
          
        self.setLayout(layout)
        self.setStyleSheet("background-color: #000000;")

    def update_data(self):
        for key, widget in self.ui_elements.items():
            try:
                widget.update_data()
            except Exception as e: 
                print(f"Error while Update: {key}: {e}")
              
