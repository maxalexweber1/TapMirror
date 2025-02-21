import sys
from PyQt5.QtWidgets import QApplication
from ui import TapMirrorUI
from api.api import get_portfolio_trade_history 


def main():
   response = get_portfolio_trade_history("stake1uxhvr22njt6fvq8jwyv958vcc9r2pa8q8zwk9t5nxvlfe7sz82fr7")
   print(response)
if __name__ == "__main__":
    main()