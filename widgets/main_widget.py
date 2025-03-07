from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QApplication
from PyQt5.QtCore import Qt
from widgets.style_manager import StyleManager
from widgets.grid_widget import GridWidget
from widgets.header_widget import HeaderWidget

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.style_manager = StyleManager()
        self.config = self.style_manager.get_layout_config()
        self.initUI()
        self.setStyleSheet("background-color: black; color: white;")
        print("Starting TapMirror..")
        print("Loading API Data...")
        self.update_data()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.header_config = self.config.get("header_sections", [])
        self.grid_config = self.config.get("grid_sections", [])

        if self.header_config:
            header_frame = QFrame()
            header_frame.setStyleSheet("border: 1px solid gray; border-radius: 5px; background-color: #000000")
            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(0, 0, 0, 0)

            self.header = HeaderWidget(self.header_config)
            self.header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            header_layout.addWidget(self.header)
            header_frame.setLayout(header_layout)

            header_frame.setMaximumHeight(self.header.sizeHint().height())
            layout.addWidget(header_frame, alignment=Qt.AlignTop)

        if self.grid_config:
            self.grid_widget = GridWidget(self.grid_config)
            self.grid_widget.setStyleSheet("border: 1px solid gray; border-radius: 5px; background-color: #000000")
            layout.addWidget(self.grid_widget, alignment=Qt.AlignTop)
            layout.addStretch(1)  

        self.setLayout(layout)

    def update_data(self):
        if hasattr(self, 'header') and self.header:
            self.header.update_data()
        if hasattr(self, 'grid_widget') and self.grid_widget:
            self.grid_widget.update_data()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        else:
            super().keyPressEvent(event)