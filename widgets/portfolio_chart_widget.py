import pandas as pd
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class PortfolioChartWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.update_chart([])
 
    def update_chart(self, data):
        """creates a price chart based on a data frame"""
        df = pd.DataFrame(data)
         
        if df.empty:
            self.setText("No data available")
            return
        df["time"] = pd.to_datetime(df["time"])

        fig, ax = plt.subplots(figsize=(6, 3))
        fig.patch.set_facecolor("#000000")
        ax.set_facecolor("#1A1A1A")
        ax.plot(df["time"], df["value"],
            color="white",
            marker="o",
            linestyle="-",
            lw=7,
            solid_capstyle="round",
            solid_joinstyle="round")
        ax.axis('off')
       
        canvas = FigureCanvas(fig)
        canvas.draw()
        width, height = canvas.get_width_height()
        buf = canvas.buffer_rgba() 
        img = QImage(buf, width, height, width * 4, QImage.Format_RGBA8888)
        pix = QPixmap.fromImage(img)
       
        scaled_pix = pix.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pix)
        matplotlib.pyplot.close()