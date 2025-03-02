from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from config.config import TOKEN_ID_MAPPING
from datetime import datetime
from api.taptools_api import get_loans_by_id
from widgets.style_manager import StyleManager
import os


class TokenLoansWidget(QWidget):
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
        color = self.style_manager.get_style("token_loans", "color", "white")
        header_size = self.style_manager.get_scaled_header_size("token_loans")
        
        self.loan_table = QGridLayout()
        headers = ["Token", "Exp. in", "Dept", "Collateral", "Health", "Protocol"]
        for col_idx, header in enumerate(headers):
            loan_header_label = QLabel(header)
            loan_header_label.setStyleSheet(f"font-size: {header_size}px; color: {color}; font-weight: bold;")
            loan_header_label.setAlignment(Qt.AlignLeft)
            self.loan_table.addWidget(loan_header_label, 0, col_idx)
      
        layout.addLayout(self.loan_table)
        self.setLayout(layout)

    def update_data(self):
        
        font_size = self.style_manager.get_scaled_font_size("token_loans")
        color = self.style_manager.get_style("token_loans", "color", "white")
        loan_count = self.config.get("count", 5)
        ticker = self.config.get("ticker", "ADA")
        token_id = TOKEN_ID_MAPPING.get(ticker, "Unknown")
        
        loan_data = get_loans_by_id(token_id, "expiration", "desc", 1, 100)
        loans = NextExpLoans(loan_data).loans

        loans = loans[:loan_count]
        
        if not loans:
            return
        
        for row_idx, loan in enumerate(loans, start=1):
            self._add_loan_row(loan, row_idx, font_size, color, ticker)

    def _clear_table(self):
        for i in reversed(range(self.loan_table.count())):
            item = self.loan_table.itemAt(i)
            row, col, rowSpan, colSpan = self.loan_table.getItemPosition(i)
            if row > 0:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                    self.loan_table.removeWidget(widget)

    def _add_loan_row(self, loan, row_idx, font_size, color, ticker):
        image_label = QLabel()
        image_path = f"assets/token/{ticker}.png"
        image_scale = self.style_manager.get_scaled_value("token_loans", "image_size", 60)
        
        pixmap = QPixmap(image_scale, image_scale)
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(image_scale, image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        self.loan_table.addWidget(image_label, row_idx, 0)
        
        now = datetime.now()
        exp_time = datetime.fromtimestamp(loan.expiration)
        delta_time = (exp_time - now).total_seconds()
        time_to = f"in {round(delta_time / 86400)} days"
        
        health_value = float(loan.health)
        if health_value < 1.2:
            health_color = "red"
        elif health_value < 2:
            health_color = "yellow"
        else:
            health_color = "green"
        
        formatted_collateral = StyleManager.format_number(round(float(loan.colateralAmount)))
        
        labels = [
            (time_to, 1),
            (f"{round(float(loan.debtAmount))} ₳", 2),
            (f"{formatted_collateral} ( {round(float(loan.collateralValue))} ₳ )", 3),
            (f"{round(float(loan.health),2)}", 4, health_color),
            (f"{loan.protocol}", 5)]
        
        for label_data in labels:
            text = label_data[0]
            col_idx = label_data[1]
            label_color = label_data[2] if len(label_data) > 2 else color
            
            label = QLabel(text)
            label.setStyleSheet(f"font-size: {font_size}px; color: {label_color};")
            label.setAlignment(Qt.AlignLeft)
            self.loan_table.addWidget(label, row_idx, col_idx)

class NextExpLoans:
    def __init__(self, data):
        self.loans = [Loan(tr) for tr in data]
        self.loans.sort(key=lambda loan: loan.expiration)
        

class Loan:
    def __init__(self, data):
        self.tokenName = data.get("tokenName", "Unknown")
        self.colateralAmount = data.get("collateralAmount", 0)
        self.collateralValue = data.get("collateralValue", 0)
        self.debtAmount = data.get("debtAmount", 0)
        self.expiration = data.get("expiration", 0)
        self.health = data.get("health", 0)
        self.protocol = data.get("protocol", "Unknown")
