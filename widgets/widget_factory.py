from widgets.clock_widget import ClockWidget
from widgets.market_data_widget import MarketDataWidget
from widgets.token_widget import TokenWidget
from widgets.portfolio_widget import PortfolioWidget
from widgets.token_trades_widget import TokenTradesWidget
from widgets.weather_widget import WeatherWidget
from widgets.token_loans_widget import TokenLoansWidget
from widgets.rss_feed_widget import MediumRSSWidget
from widgets.welcome_widget import WelcomeWidget

class WidgetFactory:
    """Factory class to dynamically create widgets based on their type."""

    widget_mapping = {
        "clock": ClockWidget,
        "marketdata": MarketDataWidget,
        "tokens": TokenWidget,
        "portfolio": PortfolioWidget,
        "token_trades": TokenTradesWidget,
        "weather": WeatherWidget,
        "token_loans": TokenLoansWidget,
        "rssfeed": MediumRSSWidget,
        "welcome": WelcomeWidget,
    }

    @staticmethod
    def create_widget(widget_type, config):
        """Creates a widget instance dynamically based on the type."""
        widget_class = WidgetFactory.widget_mapping.get(widget_type)
        if widget_class:
            return widget_class(config)
        else:
            print("Warning: No widget found for type '{widget_type}'")
            return None
