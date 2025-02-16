import pandas as pd
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class ChartWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(800, 400)  # Größe anpassen
        self.update_chart([])  # Initiales Chart mit leeren Daten

    def update_chart(self, data):
        """Erstellt ein Preisdiagramm basierend auf API-Daten."""
        df = pd.DataFrame(data)
            # Check if the DataFrame is empty
        if df.empty:
            self.setText("Keine Daten verfügbar")
            return

        if "date" not in df.columns:
            self.setText("Die erforderliche 'date'-Spalte fehlt in den Daten.")
            return

        df["date"] = pd.to_datetime(df["date"])

    # Matplotlib-Plot erstellen
        fig, ax = plt.subplots(figsize=(6, 3))
        # Setze den Hintergrund von Figure und Axes auf schwarz
        fig.patch.set_facecolor("black")
        ax.set_facecolor("black")
        ax.plot(df["date"], df["close"],
            color="white",
            label="Close",
            marker="o",
            linestyle="-",
            lw=5,
            solid_capstyle="round",
            solid_joinstyle="round")
        ax.axis('off')
        # Speichern des Bildes in QPixmap für QLabel
        canvas = FigureCanvas(fig)
        canvas.draw()
        width, height = canvas.get_width_height()
        buf = canvas.buffer_rgba()  # returns a memoryview
        img = QImage(buf, width, height, width * 4, QImage.Format_RGBA8888)
        pix = QPixmap.fromImage(img)
       # Pixmap skalieren, damit es ins Widget passt
        scaled_pix = pix.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pix)
        matplotlib.pyplot.close()