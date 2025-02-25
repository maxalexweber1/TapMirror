import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from widgets.header_widget import HeaderWidget 
from widgets.grid_widget import GridWidget

def load_layout_config():
    with open("./config/layout_config.json", "r") as file:
        return json.load(file)

class MainWidget(QWidget):
   
    def __init__(self):
        super().__init__()
        self.config = load_layout_config()
        self.initUI()

    def initUI(self):

        header = self.config.get("header_sections")
        grid = self.config.get("grid_sections")

        layout = QVBoxLayout()
        layout.setSpacing(3)
        
        if header:
            header = HeaderWidget(header)
            layout.addWidget(header)
        if grid:
            grid = GridWidget(grid)
            layout.addWidget(grid)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #000000;")

def keyPressEvent(self, event):
    if event.key() == Qt.Key_Escape:
        self.close()