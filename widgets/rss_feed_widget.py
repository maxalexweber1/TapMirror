import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy
from PyQt5.QtCore import QTimer, Qt
from widgets.style_manager import StyleManager
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
        self.style_manager = StyleManager()
        self.initUI()

        # Get and set refresh interval
        refresh = self.config.get("refresh", 600000)
        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(refresh)

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.color = self.style_manager.get_style("rssfeed", "color", "white")
        self.font_size = self.style_manager.get_scaled_font_size("rssfeed")
        self.setLayout(self.main_layout)

    def update_data(self):

        self.clear_layout(self.main_layout)

        feedname = self.config.get("name", "TapInWithTapTools")
        feed_num = self.config.get("feed_num", 3)
        feed_url = f"https://medium.com/feed/@{feedname}"
        try:
            feed = feedparser.parse(feed_url)
           
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
                    
                    label = QLabel(entry_text)
                    label.setStyleSheet(f"font-size: {self.font_size}px; color: {self.color};")
                    label.setWordWrap(True)
                    label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
               
                    self.main_layout.addWidget(label)

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
            error_label.setStyleSheet(f"font-size: {self.font_size}px; color: {self.color};")
            error_label.setWordWrap(True)
            self.main_layout.addWidget(error_label)
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()