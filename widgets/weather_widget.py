import os
from PyQt5.QtWidgets import QFrame, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime, timedelta
from PyQt5.QtGui import QPixmap
from api.open_meteo_api import get_weather_data
from widgets.style_manager import StyleManager

class WeatherWidget(QWidget):
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
        font_size = self.style_manager.get_scaled_font_size("weather")
        color = self.style_manager.get_style("weather", "color", "white")
        style = f"font-size: {font_size}px; color: {color};"
        pic_scale = self.style_manager.get_scaled_value("weather", "images_size", 400)
        forecast_image_scale = self.style_manager.get_scaled_value("weather", "forecast_image_size", 90)
        forecast_font_size = self.style_manager.get_scaled_font_size("weather")
        forecast_style = f"font-size: {forecast_font_size}px; color: {color};"

        # Main weather display
        self.label = QLabel("Loading")
        self.label.setStyleSheet(style)
        self.label.setAlignment(Qt.AlignCenter)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(pic_scale, pic_scale)
        self.image_label.setStyleSheet("border: none;")

        # Forecast display
        forecast_box = QHBoxLayout()
        self.forecast_labels = []
        self.forecast_images = []
        self.forecast_temps = []

        for i, day_label in enumerate(["Tomorrow", "2 Days", "7 Days"]):
            frame = QFrame()
            frame.setStyleSheet("border: 2px solid white; border-radius: 5px;")
            day_box = QVBoxLayout()
            
            label = QLabel(day_label)
            label.setStyleSheet(forecast_style)
            label.setAlignment(Qt.AlignCenter)
            day_box.addWidget(label)
            
            image_label = QLabel()
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setFixedSize(forecast_image_scale, forecast_image_scale)
            image_label.setStyleSheet("border: none;")
            day_box.addWidget(image_label, alignment=Qt.AlignCenter)

            temp_label = QLabel("Loading..")
            temp_label.setStyleSheet(forecast_style)
            temp_label.setAlignment(Qt.AlignCenter)
            day_box.addWidget(temp_label)
            
            frame.setLayout(day_box)
            forecast_box.addWidget(frame)
            self.forecast_labels.append(label)
            self.forecast_images.append(image_label)
            self.forecast_temps.append(temp_label)

        layout.addWidget(self.label)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        layout.addLayout(forecast_box)
        self.setLayout(layout)

    def _get_image_path_for_code(self, code, day=True):
        weather_map = {
            0: "clear_day.png", 1: "partly_cloudy_day.png", 2: "partly_cloudy_day.png", 3: "partly_cloudy_day.png",
            45: "fog.png", 48: "fog.png", 51: "hail.png", 53: "hail.png", 55: "hail.png", 56: "hail.png", 57: "hail.png",
            61: "rain.png", 63: "rain.png", 65: "rain.png", 66: "sleet.png", 67: "sleet.png", 71: "sleet.png",
            73: "sleet.png", 75: "sleet.png", 77: "snow.png", 85: "snow.png", 86: "snow.png",
            95: "tonado.png", 96: "tonado.png", 99: "tonado.png"
        }
        file_name = weather_map.get(code, "clear_day.png")
        return f"assets/weather/{file_name}" if day else f"assets/weather/{file_name.replace('_day', '_night')}"

    def update_data(self):
        latitude = self.config.get("latitude", 52.52)
        longitude = self.config.get("longitude", 13.41)
        forecast_image_scale = self.style_manager.get_scaled_value("weather", "forecast_image_size", 90)
        
        try:
            weather_data = get_weather_data(latitude, longitude)
            hourly = weather_data.get("hourly", {})
            times = hourly.get("time", [])
            temperatures = hourly.get("temperature_2m", [])
            weather_codes = hourly.get('weather_code', [])
            now = datetime.now()
            now_hour_str = now.strftime("%Y-%m-%dT%H:00")
            
            # Live weather update
            if now_hour_str in times:
                index = times.index(now_hour_str)
                temperature = temperatures[index]
                weather_code = weather_codes[index]
                self.label.setText(f"{temperature}°C")
                image_path = self._get_image_path_for_code(weather_code, now.hour > 6 and now.hour < 18)
                if os.path.exists(image_path):
                    self.image_label.setPixmap(QPixmap(image_path).scaled(forecast_image_scale, forecast_image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            # Forecast Updates (1-day, 2-day, 7-day)
            days_ahead = [1, 2, 6]
            for i, days in enumerate(days_ahead):
                day_target = (now + timedelta(days=days)).replace(hour=12, minute=0, second=0, microsecond=0)
                day_target_str = day_target.strftime("%Y-%m-%dT%H:00")
                if day_target_str in times:
                    index = times.index(day_target_str)
                    temperature = temperatures[index]
                    weather_code = weather_codes[index]
                    image_path = self._get_image_path_for_code(weather_code, day=True)
                    if os.path.exists(image_path):
                        self.forecast_images[i].setPixmap(QPixmap(image_path).scaled(forecast_image_scale, forecast_image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    self.forecast_temps[i].setText(f"{temperature}°C")
        except Exception as e:
            self.label.setText("Error fetching weather data.")

