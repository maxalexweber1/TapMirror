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
        self.setFixedSize(800, 400)
        self.update_chart([])
        timer = QTimer(self)
        timer.timeout.connect(self.update_chart)
        timer.start(100000) 

    def update_chart(self, data):
        """creates a price chart based on a data frame"""
             
        df = pd.DataFrame(data)
         
        if df.empty:
            self.setText("No data available")
            return

        df["time"] = pd.to_datetime(df["time"])

        fig, ax = plt.subplots(figsize=(6, 3))
        fig.patch.set_facecolor("black")
        ax.set_facecolor("black")
        ax.plot(df["time"], df["value"],
            color="white",
            marker="o",
            linestyle="-",
            lw=5,
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