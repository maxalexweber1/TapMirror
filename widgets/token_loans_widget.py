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
        font_size = self.style_manager.get_scaled_font_size("token_loans")
        color = self.style_manager.get_style("token_loans", "color", "white")
        header_size = self.style_manager.get_scaled_font_size("token_loans")
        
        frame = QFrame()
        frame.setStyleSheet("border: 2px solid white; border-radius: 5px;")
        frame_layout = QVBoxLayout()
        
        self.loan_table = QGridLayout()
        headers = ["Token", "Exp. in", "Value", "Amount", "Value", "Health", "Protocol"]
        for col_idx, header in enumerate(headers):
            loan_header_label = QLabel(header)
            loan_header_label.setStyleSheet(f"font-size: {header_size}px; color: {color}; font-weight: bold;")
            loan_header_label.setAlignment(Qt.AlignCenter)
            self.loan_table.addWidget(loan_header_label, 0, col_idx)
        
        frame_layout.addLayout(self.loan_table)
        frame.setLayout(frame_layout)
        layout.addWidget(frame)
        self.setLayout(layout)

    def update_data(self):
        self._clear_table()
        
        font_size = self.style_manager.get_scaled_font_size("token_loans")
        color = self.style_manager.get_style("token_loans", "color", "white")
        loan_count = self.config.get("count", 5)
        ticker = self.config.get("ticker", "ADA")
        token_id = TOKEN_ID_MAPPING.get(ticker, "Unknown")
        
        # Re-add headers
        headers = ["Token", "Exp. in", "Value", "Amount", "Value", "Health", "Protocol"]
        for col_idx, header in enumerate(headers):
            loan_header_label = QLabel(header)
            loan_header_label.setStyleSheet(f"font-size: {font_size}px; color: {color}; font-weight: bold;")
            loan_header_label.setAlignment(Qt.AlignCenter)
            self.loan_table.addWidget(loan_header_label, 0, col_idx)
        
        loan_data = get_loans_by_id(token_id, "expiration", "desc", 1, loan_count)
        loans = NextExpLoans(loan_data).loans
        
        if not loans:
            return
        
        for row_idx, loan in enumerate(loans, start=1):
            self._add_loan_row(loan, row_idx, font_size, color)

    def _clear_table(self):
        for i in range(self.loan_table.count() - 1, -1, -1):
            item = self.loan_table.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
                self.loan_table.removeWidget(item.widget())

    def _add_loan_row(self, loan, row_idx, font_size, color):
        image_label = QLabel()
        image_path = f"assets/token/{loan.tokenName}.png"
        pic_scale = self.style_manager.get_scaled_value("token_loans", "images_size", 60)
        
        pixmap = QPixmap(pic_scale, pic_scale)
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(pic_scale, pic_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        self.loan_table.addWidget(image_label, row_idx, 0)
        
        now = datetime.now()
        exp_time = datetime.fromtimestamp(loan.expiration)
        delta_time = (exp_time - now).total_seconds()
        time_to = f"in {round(delta_time / 3600)}h"
        
        # Determine color for health value
        health_value = float(loan.health)
        if health_value < 1.2:
            health_color = "red"
        elif health_value < 2:
            health_color = "yellow"
        else:
            health_color = "green"
        
        labels = [
            (time_to, 1),
            (f"{round(float(loan.debtAmount))} ₳", 2),
            (f"{round(float(loan.colateralAmount))}", 3),
            (f"{round(float(loan.collateralValue))} ₳", 4),
            (f"{round(float(loan.health),2)}", 5, health_color),
            (f"{loan.protocol}", 6)
        ]
        
        for label_data in labels:
            text = label_data[0]
            col_idx = label_data[1]
            label_color = label_data[2] if len(label_data) > 2 else color
            
            label = QLabel(str(text))
            label.setStyleSheet(f"font-size: {font_size}px; color: {label_color};")
            label.setAlignment(Qt.AlignCenter)
            self.loan_table.addWidget(label, row_idx, col_idx)

class NextExpLoans:
    def __init__(self, data):
        self.loans = [Loan(tr) for tr in data]

class Loan:
    def __init__(self, data):
        self.tokenName = data.get("tokenName", "Unknown")
        self.colateralAmount = data.get("collateralAmount", 0)
        self.collateralValue = data.get("collateralValue", 0)
        self.debtAmount = data.get("debtAmount", 0)
        self.expiration = data.get("expiration", 0)
        self.health = data.get("health", 0)
        self.protocol = data.get("protocol", "Unknown")
