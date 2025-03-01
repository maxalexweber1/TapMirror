import sys
from PyQt5.QtWidgets import QApplication
from widgets.main_widget import MainWidget
from PyQt5.QtCore import Qt

if __name__ == "__main__":
    """ Start of Main Logic """
    app = QApplication(sys.argv)
    window = MainWidget()
    window.setWindowTitle("TapMirror")
    window.showFullScreen()
    sys.exit(app.exec_())

def keyPressEvent(self, event):
    '''Beende die Anwendung bei Drücken der Esc-Taste'''
    if event.key() == Qt.Key_Escape:
        QApplication.quit()
