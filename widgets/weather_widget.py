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
        self.update_data()  # Initial update

        refresh = self.config.get("refresh", 100000)  # Default: 100 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(refresh)

    def initUI(self):
        layout = QVBoxLayout()

        header_size = self.style_manager.get_scaled_header_size("weather")
        color = self.style_manager.get_style("weather", "color", "white")
        style = f"font-size: {header_size}px; color: {color};"
        image_size = self.style_manager.get_scaled_image_size("weather", "image_size")
        forecast_image_scale = self.style_manager.get_scaled_image_size("weather", "fc_image_size")
        forecast_font_size = self.style_manager.get_scaled_font_size("weather")
        forecast_style = f"font-size: {forecast_font_size}px; color: {color};"

        inner_widgets = self.config.get("innerWidgets", ["current", "forecast"])
    
        if "current" in inner_widgets:

            current_box = QHBoxLayout()
        
            self.current_label = QLabel("Loading...")
            self.current_label.setStyleSheet(style)
            self.current_label.setAlignment(Qt.AlignCenter)
            current_box.addWidget(self.current_label)

            self.current_image_label = QLabel()
            self.current_image_label.setAlignment(Qt.AlignCenter)
            self.current_image_label.setFixedSize(image_size, image_size)
            self.current_image_label.setStyleSheet(style)
            current_box.addWidget(self.current_image_label, alignment=Qt.AlignCenter)

            current_box.setContentsMargins(5, 5, 5, 5)  
            current_box.setSpacing(10)  

            layout.addLayout(current_box)

        if "forecast" in inner_widgets:
            forecast_frame = QFrame()
            forecast_frame.setStyleSheet(forecast_style)
            forecast_box = QHBoxLayout()

            self.forecast_labels = []
            self.forecast_images = []
            self.forecast_temps = []

            for i, day_label in enumerate(["Tomorrow", "2 Days", "3 Days"]):
                day_box = QVBoxLayout()

                label = QLabel(day_label)
                label.setStyleSheet(forecast_style)
                label.setAlignment(Qt.AlignCenter)
                day_box.addWidget(label)

                image_label = QLabel()
                image_label.setAlignment(Qt.AlignCenter)
                image_label.setFixedSize(forecast_image_scale, forecast_image_scale)
                image_label.setStyleSheet(forecast_style) 
                day_box.addWidget(image_label, alignment=Qt.AlignCenter)

                temp_label = QLabel("Loading...")
                temp_label.setStyleSheet(forecast_style)
                temp_label.setAlignment(Qt.AlignCenter)
                day_box.addWidget(temp_label)

               
                day_box.setContentsMargins(0, 0, 0, 0)  
                day_box.setSpacing(5)  

                forecast_box.addLayout(day_box)
                self.forecast_labels.append(label)
                self.forecast_images.append(image_label)
                self.forecast_temps.append(temp_label)

            forecast_box.setContentsMargins(5, 5, 5, 5)  
            forecast_box.setSpacing(10)  

            forecast_frame.setLayout(forecast_box)
            layout.addWidget(forecast_frame)

        layout.addStretch(1) 
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
        """Updates the prices, charts and change values of the tokens"""
        latitude = self.config.get("geo", [52.52, 13.4])[0]
        longitude = self.config.get("geo", [52.52, 13.4])[1]
        image_scale = self.style_manager.get_scaled_image_size("weather", "image_size")
        forecast_image_scale = self.style_manager.get_scaled_image_size("weather", "fc_image_size")

        try:
            weather_data = get_weather_data(latitude, longitude)
            if not weather_data:
                raise ValueError("No weather data returned")

            hourly = weather_data.get("hourly", {})
            times = hourly.get("time", [])
            temperatures = hourly.get("temperature_2m", [])
            weather_codes = hourly.get("weather_code", [])
            now = datetime.now()
            now_hour_str = now.strftime("%Y-%m-%dT%H:00")

            if "current" in self.config.get("innerWidgets", ["current"]):
                if now_hour_str in times:
                    index = times.index(now_hour_str)
                    temperature = temperatures[index]
                    weather_code = weather_codes[index]
                    self.current_label.setText(f"{temperature}°C")
                    image_path = self._get_image_path_for_code(weather_code, now.hour > 6 and now.hour < 18)
                    if os.path.exists(image_path):
                        pixmap = QPixmap(image_path).scaled(image_scale, image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.current_image_label.setPixmap(pixmap)
                    else:
                        self.current_label.setText(f"Image not found: {image_path}")

            if "forecast" in self.config.get("innerWidgets", ["forecast"]) and self.forecast_images:
                days_ahead = [1, 2, 3]
                for i, days in enumerate(days_ahead):
                    day_target = (now + timedelta(days=days)).replace(hour=12, minute=0, second=0, microsecond=0)
                    day_target_str = day_target.strftime("%Y-%m-%dT%H:00")
                    if day_target_str in times:
                        index = times.index(day_target_str)
                        temperature = temperatures[index]
                        weather_code = weather_codes[index]
                        image_path = self._get_image_path_for_code(weather_code, day=True)
                        self.forecast_temps[i].setText(f"{temperature}°C")
                        if os.path.exists(image_path):
                            pixmap = QPixmap(image_path).scaled(forecast_image_scale, forecast_image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            self.forecast_images[i].setPixmap(pixmap)
                        else:
                            self.forecast_temps[i].setText(f"Image not found: {image_path}")
        except Exception as e:
            self.current_label.setText(f"Error: {str(e)}")