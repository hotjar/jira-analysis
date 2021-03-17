class ChartError(Exception):
    """Raised whenever we have a generic error trying to draw the chart."""


class NoTicketsProvided(ChartError):
    """Raised if we provide no tickets to the chart."""

    def __init__(self) -> None:
        super().__init__("No tickets provided. Check your config.")
