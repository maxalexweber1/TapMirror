import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy
from PyQt5.QtCore import QTimer, Qt
import feedparser

def clean_text(html_text):
    '''Delete HTML tags from input'''
    return re.sub('<[^<]+?>', '', html_text)

def truncate_text(text, max_chars=500):
    '''Truncate text to a maximum number of characters'''
    if len(text) <= max_chars:
        return text
    last_period = text.rfind('.', 0, max_chars)
    if last_period != -1:
        return text[:last_period + 1] + "..."
    else:
        return text[:max_chars] + "..."

class MediumRSSWidget(QWidget):
    '''Widget to show Medium Article Feed'''
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()

        # Get and set refresh interval
        refresh = self.config.get("refresh", 60000)
        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(refresh)

    def initUI(self):
        self.main_layout = QVBoxLayout()
        font_size = self.config.get("font_size", 14)
        color = self.config.get("color", "black")
        self.label_style = f"font-size: {font_size}px; color: {color}; background-color: transparent; border: none;"
        self.frame_style = "border: 2px solid white; border-radius: 5px;"
        self.setLayout(self.main_layout)

        # Bildschirmbreite als Referenz
        self.screen_width = QApplication.primaryScreen().size().width()

        # Setze Größenpolitik und Breite
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.setFixedWidth(self.screen_width)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_data(self):
        feedname = self.config.get("name", "TapInWithTapTools")
        feed_num = self.config.get("feed_num", 3)
        feed_url = f"https://medium.com/feed/@{feedname}"
        try:
            feed = feedparser.parse(feed_url)
            self.clear_layout(self.main_layout)
            # Aktualisiere die Breite basierend auf dem Eltern-Widget
            if self.parent():
                self.setFixedWidth(self.screen_width)
            if feed.entries:
                entries = feed.entries[:feed_num]
                for i, entry in enumerate(entries):
                    title = entry.get("title", "No Title")
                    published = entry.get("published", "No Date")
                    summary = entry.get("summary", "No Summary")
                    clean_summary = clean_text(summary)
                    truncated_summary = truncate_text(clean_summary, 500)
                    cut_summary = truncated_summary[9:]
                    entry_text = (f"<b>{title}</b><br>"
                                  f"Published: {published}<br><br>"
                                  f"{cut_summary}")
                    
                    frame = QFrame()
                    frame.setStyleSheet(self.frame_style)
                    frame_layout = QVBoxLayout()
                    #fr"ame_layout.setContentsMargins(5, 5, 5, 5)
                    label = QLabel(entry_text)
                    label.setStyleSheet(self.label_style)
                    label.setWordWrap(True)
                    label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    label.setFixedWidth(self.screen_width - 10)  # Minus Innenränder
                    frame_layout.addWidget(label)

                    frame.setLayout(frame_layout)
                    frame.setFixedWidth(self.screen_width)
                    self.main_layout.addWidget(frame)

                    if i < len(entries) - 1:
                        self.main_layout.addSpacing(15)
            else:
                no_feed_label = QLabel("No Feed-Entries found.")
                no_feed_label.setStyleSheet(self.label_style)
                no_feed_label.setFixedWidth(self.screen_width - 10)
                no_feed_label.setWordWrap(True)
                self.main_layout.addWidget(no_feed_label)
        except Exception as e:
            error_label = QLabel(f"Error Loading RSS Feed: {str(e)}")
            error_label.setStyleSheet(self.label_style)
            error_label.setFixedWidth(self.screen_width - 10)
            error_label.setWordWrap(True)
            self.main_layout.addWidget(error_label)

    def resizeEvent(self, event):
        if self.parent():
            new_width = min(self.parent().width(), self.screen_width // 2)
            self.setFixedWidth(new_width)
            for i in range(self.main_layout.count()):
                item = self.main_layout.itemAt(i)
                if item.widget():
                    widget = item.widget()
                    if isinstance(widget, QFrame):
                        widget.setFixedWidth(new_width)
                        layout = widget.layout()
                        if layout and layout.count():
                            label = layout.itemAt(0).widget()
                            if label:
                                label.setFixedWidth(new_width - 10)
        super().resizeEvent(event)