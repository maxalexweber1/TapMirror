import sys
from PyQt5.QtWidgets import QApplication
from ui import TapMirrorUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TapMirrorUI()
    sys.exit(app.exec_())