import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime, timedelta
from PyQt5.QtGui import QPixmap
from api.open_meteo_api import get_weather_data

class WeatherWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()

        refresh = self.config.get("refresh", 100000)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(refresh)
        self.update_data() 

    def initUI(self):
        layout = QVBoxLayout()
        color = self.config.get("color", "white")

        # Einstellungen für die Hauptanzeige (Temperatur)
        font_size = self.config.get("font_size", 80)
        style = f"font-size: {font_size}px; color: {color};"

        # Einstellungen für die Forecastanzeige
        forecast_image_scale = self.config.get("forecast_image_size", 90)
        forecast_font_size = self.config.get("forecast_font_size", 20)
        forecast_style = f"font-size: {forecast_font_size}px; color: {color};"

        # Layout für die aktuelle Wetteranzeige
        first_row_layout = QHBoxLayout()
        self.label = QLabel("Loading")
        self.label.setStyleSheet(style)
        self.label.setAlignment(Qt.AlignCenter)
        first_row_layout.addWidget(self.label)

        pic_scale = self.config.get("images_size", 400)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        image_path = "assets/weather/clear_day.png"
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(pic_scale, pic_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("[No Image]")
            self.image_label.setFixedSize(pic_scale, pic_scale)
        first_row_layout.addWidget(self.image_label)
        layout.addLayout(first_row_layout)  # Korrekt: addLayout statt addWidget

        # Layout für die Forecastanzeige
        forecast_box = QHBoxLayout()

        # Forecast: Tomorrow
        self.f1_daybox = QVBoxLayout()
        self.f1_label = QLabel("Tomorrow")
        self.f1_label.setStyleSheet(forecast_style)
        self.f1_label.setAlignment(Qt.AlignCenter)
        self.f1_daybox.addWidget(self.f1_label)

        self.f1_image_label = QLabel()
        self.f1_image_label.setAlignment(Qt.AlignCenter)
        self.f1_image_path = "assets/weather/clear_day.png"
        if os.path.exists(self.f1_image_path):
            pixmap = QPixmap(self.f1_image_path).scaled(forecast_image_scale, forecast_image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.f1_image_label.setPixmap(pixmap)
        else:
            self.f1_image_label.setText("[No Image]")
            self.f1_image_label.setFixedSize(forecast_image_scale, forecast_image_scale)
        self.f1_daybox.addWidget(self.f1_image_label)

        self.f1_temp_label = QLabel("Loading..")
        self.f1_temp_label.setStyleSheet(forecast_style)
        self.f1_temp_label.setAlignment(Qt.AlignCenter)
        self.f1_daybox.addWidget(self.f1_temp_label)
        forecast_box.addLayout(self.f1_daybox)

        # Forecast: 2 Days
        self.f2_daybox = QVBoxLayout()
        self.f2_label = QLabel("2 Days")
        self.f2_label.setStyleSheet(forecast_style)
        self.f2_label.setAlignment(Qt.AlignCenter)
        self.f2_daybox.addWidget(self.f2_label)

        self.f2_image_label = QLabel()
        self.f2_image_label.setAlignment(Qt.AlignCenter)
        self.f2_image_path = "assets/weather/clear_day.png"
        if os.path.exists(self.f2_image_path):
            pixmap = QPixmap(self.f2_image_path).scaled(forecast_image_scale, forecast_image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.f2_image_label.setPixmap(pixmap)
        else:
            self.f2_image_label.setText("[No Image]")
            self.f2_image_label.setFixedSize(forecast_image_scale, forecast_image_scale)
        self.f2_daybox.addWidget(self.f2_image_label)

        self.f2_temp_label = QLabel("Loading..")
        self.f2_temp_label.setStyleSheet(forecast_style)
        self.f2_temp_label.setAlignment(Qt.AlignCenter)
        self.f2_daybox.addWidget(self.f2_temp_label)
        forecast_box.addLayout(self.f2_daybox)

        # Forecast: 7 Days
        self.f3_daybox = QVBoxLayout()
        self.f3_label = QLabel("7 Days")
        self.f3_label.setStyleSheet(forecast_style)
        self.f3_label.setAlignment(Qt.AlignCenter)
        self.f3_daybox.addWidget(self.f3_label)

        self.f3_image_label = QLabel()
        self.f3_image_label.setAlignment(Qt.AlignCenter)
        self.f3_image_path = "assets/weather/clear_day.png"
        if os.path.exists(self.f3_image_path):
            pixmap = QPixmap(self.f3_image_path).scaled(forecast_image_scale, forecast_image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.f3_image_label.setPixmap(pixmap)
        else:
            self.f3_image_label.setText("[No Image]")
            self.f3_image_label.setFixedSize(forecast_image_scale, forecast_image_scale)
        self.f3_daybox.addWidget(self.f3_image_label)

        self.f3_temp_label = QLabel("Loading")
        self.f3_temp_label.setStyleSheet(forecast_style)
        self.f3_temp_label.setAlignment(Qt.AlignCenter)
        self.f3_daybox.addWidget(self.f3_temp_label)
        forecast_box.addLayout(self.f3_daybox)

        layout.addLayout(forecast_box)
        self.setLayout(layout)

#WMO Weather interpretation codes (WW)
#Code	Description
#0	Clear sky
#1, 2, 3	Mainly clear, partly cloudy, and overcast
#45, 48	Fog and depositing rime fog
#51, 53, 55	Drizzle: Light, moderate, and dense intensity
#56, 57	Freezing Drizzle: Light and dense intensity
#61, 63, 65	Rain: Slight, moderate and heavy intensity
#66, 67	Freezing Rain: Light and heavy intensity
#71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
#77	Snow grains
#80, 81, 82	Rain showers: Slight, moderate, and violent
#85, 86	Snow showers slight and heavy
#95 *	Thunderstorm: Slight or moderate
#96, 99 *	Thunderstorm with slight and heavy hail
    def _get_image_path_for_code(self, code, day=True):
     match code:
        case 0:
            return "assets/weather/clear_day.png" if day else "assets/weather/clear_night.png"
        case 1 | 2 | 3:
            return "assets/weather/partly_cloudy_day.png" if day else "assets/weather/partly_cloudy_night.png"
        case 45 | 48:
            return "assets/weather/fog.png"
        case 51 | 53 | 55 | 56 | 57 | 80 | 81 | 82:
            return "assets/weather/hail.png"
        case 61 | 63 | 65:
            return "assets/weather/rain.png"
        case 66 | 67 | 71 | 73 | 75:
            return "assets/weather/sleet.png"
        case 77 | 85 | 86:
            return "assets/weather/snow.png"
        case 95 | 96 | 99:
            return "assets/weather/tonado.png"
        case _:
            return "assets/weather/clear_day.png"

    def update_data(self):
        latitude = self.config.get("latitude", 52.52)
        longitude = self.config.get("longitude", 13.41)
        forecast_image_scale = self.config.get("forecast_image_size", 90)
        try:
            weather_data = get_weather_data(latitude, longitude)
            hourly = weather_data.get("hourly", {})
            times = hourly.get("time", [])
            temperatures = hourly.get("temperature_2m", [])
            weather_codes = hourly.get('weather_code',[])

            now = datetime.now()
            now_hour_str = now.strftime("%Y-%m-%dT%H:00")
            temperature = None
            # live wether
            if now_hour_str in times:
                index = times.index(now_hour_str)
                temperature = temperatures[index]
                weather_code = weather_codes[index]

            if temperature is not None:
                self.label.setText(f"{temperature}°C")
            else:
                self.label.setText("Keine Temperaturdaten verfügbar.")

            # update live weather picture
            if weather_code is not None:
   
                if now.hour > 6 and now.hour < 18:
                    image_path = self._get_image_path_for_code(weather_code, day=True)
                else:
                    image_path = self._get_image_path_for_code(weather_code, day=False)
                    
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path).scaled(forecast_image_scale, forecast_image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.image_label.setPixmap(pixmap)
            
            one_day = ( now + timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)
            one_day_str = one_day.strftime("%Y-%m-%dT%H:00")
            two_day = ( now + timedelta(days=2)).replace(hour=12, minute=0, second=0, microsecond=0)
            two_day_str = two_day.strftime("%Y-%m-%dT%H:00")
            seven_day = ( now + timedelta(days=6)).replace(hour=12, minute=0, second=0, microsecond=0)
            seven_day_str = seven_day.strftime("%Y-%m-%dT%H:00")
           
        # Update Tomorrow 
            if one_day_str in times:
                index = times.index(one_day_str)
                temperature = temperatures[index]
                weather_code = weather_codes[index]
                image_path = self._get_image_path_for_code(weather_code, day=True)
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path).scaled(forecast_image_scale, forecast_image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.f1_image_label.setPixmap(pixmap)
                if temperature is not None:
                    self.f1_temp_label.setText(f"{temperature}°C")
            # update 2 Days
            if two_day_str in times:
                index = times.index(two_day_str)
                temperature = temperatures[index]
                weather_code = weather_codes[index]
                image_path = self._get_image_path_for_code(weather_code, day=True)
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path).scaled(forecast_image_scale, forecast_image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.f2_image_label.setPixmap(pixmap)
                if temperature is not None:
                    self.f2_temp_label.setText(f"{temperature}°C")    
            # update 7 Days
            if seven_day_str in times:
                index = times.index(seven_day_str)
                temperature = temperatures[index]
                weather_code = weather_codes[index]
                image_path = self._get_image_path_for_code(weather_code, day=True)
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path).scaled(forecast_image_scale, forecast_image_scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.f3_image_label.setPixmap(pixmap)
                if temperature is not None:
                    self.f3_temp_label.setText(f"{temperature}°C")

        except Exception as e:
            self.label.setText("Fehler beim Laden der Wetterdaten.")