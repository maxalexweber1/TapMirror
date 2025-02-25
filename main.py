import sys
from PyQt5.QtWidgets import QApplication
from widgets.main_widget import MainWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWidget()
    window.setWindowTitle("TapMirror")
    window.showFullScreen()
    sys.exit(app.exec_())


