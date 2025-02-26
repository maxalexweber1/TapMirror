import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import QTimer, Qt
import feedparser

def clean_text(html_text):
    '''delete html tags from input'''
    return re.sub('<[^<]+?>', '', html_text)

def truncate_text(text, max_chars=500):
    '''delete html tags from input'''
    if len(text) <= max_chars:
        return text
    last_period = text.rfind('.', 0, max_chars)
    if last_period != -1:
        return text[:last_period+1] + "..."
    else:
        return text[:max_chars] + "..."

class MediumRSSWidget(QWidget):
    '''Widget to show Medium Article Feed'''
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()

        # get and set refresh intervall
        refresh = self.config.get("refresh", 60000)
        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(refresh)

    def initUI(self):
        self.main_layout = QVBoxLayout()
        font_size = self.config.get("font_size", 14)
        color = self.config.get("color", "black")
        self.style = f"font-size: {font_size}px; color: {color};"
        self.setLayout(self.main_layout)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def update_data(self):
        feedname = self.config.get("name", "TapInWithTapTools")
        feed_num = self.config.get("feed_num", 4)
        feed_url = f"https://medium.com/feed/@{feedname}"
        try:
            feed = feedparser.parse(feed_url)
            self.clear_layout(self.main_layout)
            if feed.entries:
                entries = feed.entries[:feed_num]
                for entry in entries:
                    title = entry.get("title", "No Title")
                    published = entry.get("published", "No Date")
                    summary = entry.get("summary", "No Summary")
                    clean_summary = clean_text(summary)
                    truncated_summary = truncate_text(clean_summary, 500)
                    # clear date from summary
                    cut_summary = truncated_summary[9:]
                    entry_text = (f"<b>{title}</b><br>"
                                  f"Published: {published}<br><br>"
                                  f"{cut_summary}")
                    
                    frame = QFrame()
                    frame_layout = QVBoxLayout()
                    label = QLabel(entry_text)
                    label.setStyleSheet(self.style)
                    label.setWordWrap(True)
                    label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
                    frame_layout.addWidget(label)
                    frame.setLayout(frame_layout)
                    frame.setFrameShape(QFrame.StyledPanel)
                    
                    self.main_layout.addWidget(frame)
            else:
                no_feed_label = QLabel("No Feed-Entries found.")
                no_feed_label.setStyleSheet(self.style)
                self.main_layout.addWidget(no_feed_label)
        except Exception as e:
            error_label = QLabel("Error Loading RSS Feed")
            error_label.setStyleSheet(self.style)
            self.main_layout.addWidget(error_label)

