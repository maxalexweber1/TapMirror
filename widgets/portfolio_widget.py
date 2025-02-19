from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class PortfolioWidget(QWidget):
    def __init__(self, config, portfolio_data):
        super().__init__()
        self.config = config
        self.portfolio_data = portfolio_data
        self.token_widgets = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        font_size = self.config.get("font_size", 50)
        color = self.config.get("color", "white")
        style = f"font-size: {font_size}px; color: {color};"

        inner_widgets = self.config.get("innerWidgets", [])
        if "adabalance" in inner_widgets:
            self.balance_label = QLabel("Loading...")
            self.balance_label.setStyleSheet(style)
            self.balance_label.setAlignment(Qt.AlignVCenter)
            layout.addWidget(self.balance_label)

        if "adavalue" in inner_widgets:
            self.value_label = QLabel("Loading...")
            self.value_label.setStyleSheet(style)
            self.value_label.setAlignment(Qt.AlignVCenter)
            layout.addWidget(self.value_label)

        if "tokens" in inner_widgets:
            self.token_table = QGridLayout()
            headers = ["Balance", "Ticker", "Price", "Value", "Change 24h", "Change 7d", "Change 30d"]
            for col_idx, header in enumerate(headers):
                header_label = QLabel(header)
                header_label.setStyleSheet(f"{style} font-weight: bold;")
                header_label.setAlignment(Qt.AlignCenter)
                self.token_table.addWidget(header_label, 0, col_idx)
            layout.addLayout(self.token_table)

        self.setLayout(layout)

    def update_data(self, portfolio):
        if hasattr(self, "balance_label"):
            ada_balance = round(float(portfolio.ada_balance))
            self.balance_label.setText(f"Balance: {ada_balance} ₳")
        if hasattr(self, "value_label"):
            ada_value = round(float(portfolio.ada_value))
            self.value_label.setText(f"Portfolio Value: {ada_value} ₳")
        if hasattr(self, "token_table"):
            # Entferne alte Zeilen (außer Überschriften)
            for i in range(self.token_table.rowCount() - 1, 0, -1):
                for j in range(self.token_table.columnCount()):
                    item = self.token_table.itemAtPosition(i, j)
                    if item:
                        widget = item.widget()
                        if widget:
                            widget.deleteLater()
                            self.token_table.removeWidget(widget)

            # Neue Token-Zeilen hinzufügen
            row_idx = 1
            for token in portfolio.positions_ft:
                if token.ticker == 'ADA':
                    continue
                balance_label = QLabel(str(round(float(token.balance), 2)) if token.balance else "N/A")
                balance_label.setStyleSheet("font-size: 50px; color: white;")
                self.token_table.addWidget(balance_label, row_idx, 0)

                ticker_label = QLabel(token.ticker)
                ticker_label.setStyleSheet("font-size: 50px; color: white;")
                self.token_table.addWidget(ticker_label, row_idx, 1)

                price_label = QLabel(f"{round(float(token.price), 4)} ₳" if token.price else "N/A")
                price_label.setStyleSheet("font-size: 50px; color: white;")
                self.token_table.addWidget(price_label, row_idx, 2)

                value_label = QLabel(f"{round(float(token.ada_value), 2)} ₳" if token.ada_value else "N/A")
                value_label.setStyleSheet("font-size: 50px; color: white;")
                self.token_table.addWidget(value_label, row_idx, 3)

                change24_label = QLabel(f"{round(float(token.change_24h) * 100, 2)}%" if token.change_24h else "N/A")
                change24_label.setStyleSheet("font-size: 50px; color: white;")
                self.token_table.addWidget(change24_label, row_idx, 4)

                change7d_label = QLabel(f"{round(float(token.change_7d) * 100, 2)}%" if token.change_7d else "N/A")
                change7d_label.setStyleSheet("font-size: 50px; color: white;")
                self.token_table.addWidget(change7d_label, row_idx, 5)

                change30d_label = QLabel(f"{round(float(token.change_30d) * 100, 2)}%" if token.change_30d else "N/A")
                change30d_label.setStyleSheet("font-size: 50px; color: white;")
                self.token_table.addWidget(change30d_label, row_idx, 6)

                row_idx += 1