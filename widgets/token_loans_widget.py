from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from config.config import TOKEN_ID_MAPPING
from datetime import datetime
from api.taptools_api import get_loans_by_id
import os


class TokenLoansWidget(QWidget):
    BOLD_STYLE = "font-weight: bold;"

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.token_widgets = {}
        self.initUI()

        refresh = self.config.get("refresh", 100000)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(refresh)

    def initUI(self):
        layout = QVBoxLayout()
        color = self.config.get("color", "white")
        header_size = self.config["header_size"]

        self.loan_table = QGridLayout()
        headers = ["Token", "Exp. in", " Value", "Amount", "Value", "Health", "Protocol"]
        for col_idx, header in enumerate(headers):
            loan_header_label = QLabel(header)
            loan_header_label.setStyleSheet(self.get_style(header_size, color, bold=True))
            loan_header_label.setAlignment(Qt.AlignCenter)
            self.loan_table.addWidget(loan_header_label, 0, col_idx)
        layout.addLayout(self.loan_table)
        layout.addSpacing(10)
        self.setLayout(layout)

    def _add_loan_row(self, loan, row_idx, font_size, color):
        pic_scale = self.config["images_size"]
        image_label = QLabel()
        image_path = os.path.join("assets/token", f"{loan.tokenName}.png")
        pixmap = QPixmap(pic_scale, pic_scale)
        pixmap.fill(Qt.black)
        if os.path.exists(image_path):
            temp_pixmap = QPixmap(image_path)
            if not temp_pixmap.isNull():
                pixmap = temp_pixmap
        pixmap = pixmap.scaled(pic_scale, pic_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        self.loan_table.addWidget(image_label, row_idx, 0)

        now = datetime.now() 
        exp_time = datetime.fromtimestamp(loan.expiration)
        delta_time = (exp_time - now).total_seconds()

        time_to = f" in {round(delta_time / 3600 )}h" 

        labels = [
            (time_to, 1),
            (f"{round(float(loan.debtAmount))} ₳", 2),
            (f"{round(float(loan.colateralAmount))}", 3),
            (f"{round(float(loan.collateralValue))} ₳", 4),
            (f"{round(float(loan.health),2)}", 5),
            (f" {loan.protocol}", 6)
        ]

        for text, col_idx in labels:
            label = QLabel(str(text))
            label.setStyleSheet(self.get_style(font_size, color))
            self.loan_table.addWidget(label, row_idx, col_idx)

    def _clear_trade_rows(self):
        count = self.loan_table.count()
        header_count = self.loan_table.columnCount()
    
        for i in range(count - 1, header_count - 1, -1):
            item = self.loan_table.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
                self.loan_table.removeWidget(item.widget())

    def _remove_table_header(self, table):
        for col in range(table.columnCount()):
            item = table.itemAtPosition(0, col)
            if item and item.widget():
                widget = item.widget()
                widget.deleteLater()
                table.removeWidget(widget)

    def get_style(self, font_size=None, color=None, bold=False, header_size=False):
        font_size = font_size or self.config.get("font_size", 30)
        header_size = header_size or self.config.get("header_size", 20)
        color = color or self.config.get("color", "white")
        style = f"font-size: {font_size}px; color: {color};"
        if bold:
            style += f" {self.BOLD_STYLE}"
        return style

    def update_data(self):

        self._clear_trade_rows()

        font_size = self.config["font_size"]
        color = self.config["color"]
        loan_count = self.config["count"]
        ticker = self.config["ticker"]

        token_id = TOKEN_ID_MAPPING.get(ticker)
        loan_data = get_loans_by_id(token_id, "expiration", "desc", 1, loan_count )

        loans = NextExpLoans(loan_data)

        if not loans.loans:
            self._remove_table_header(self.loan_table)
        else:
            row_idx = 1
            for loan in loans.loans:
                loan.tokenName = ticker
                self._add_loan_row(loan, row_idx, font_size, color)
                row_idx += 1

class NextExpLoans:
    def __init__(self, data):
        self.loans = [Loan(tr) for tr in data]

class Loan:
    def __init__(self, data):
        self.tokenName = ""
        self.colateralAmount = data.get("collateralAmount")
        self.colateralToken = data.get("collateralToken")
        self.collateralValue = data.get("collateralValue")
        self.debtAmount = data.get("debtAmount")
        self.expiration = data.get("expiration")
        self.health = data.get("health")
        self.protocol = data.get("protocol")

